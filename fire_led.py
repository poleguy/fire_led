# the first one I did was this:
# https://www.thegeekpub.com/16187/controlling-ws2812b-leds-with-a-raspberry-pi/

# https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
# mocked out to work on a pc
#
# sudo nano /lib/systemd/system/led.service
# deploy changes:
# cd ~/flippy-data/2022/fire_led
# rsync -rahP ./ pi@fire.local:/home/pi/fire_led/
# rsync -rahP ~/flippy-data/2022/fire_led/ pi@fire.local:/home/pi/fire_led/



# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
#import pafy
import cv2
import time
from PIL import Image, ImageDraw
import numpy as np
#try: 
#    import board
#    import neopixel
#    mock_neopixel = False
#except ModuleNotFoundError as e:
#    print("module board or neopixels not found, using mock_neopixels")
#    import mock_board as board
#    import mock_neopixel as neopixel
#    mock_neopixel = True

# https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
if __package__ is None or __package__ == '':
    # uses current directory visibility
    import logger
else:
    # uses current package visibility
    from . import logger

logger = logger.get_logger(__name__)

    


def wheel(pos, ORDER):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait, num_pixels, order, pixels):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255, order)
        pixels.show()
        time.sleep(wait)


#https://stackoverflow.com/questions/32609098/how-to-fast-change-image-brightness-with-python-opencv
def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

# https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv/50053219#50053219
def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):
    
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

# https://stackoverflow.com/questions/237079/how-do-i-get-file-creation-and-modification-date-times
import os
import datetime
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def main(mock:bool = False):

    # if this module is imported rather than run, board and neopixel will
    # have to be imported for it to work
    global board, neopixel
    if not mock:
        import board
        import neopixel
    else:
        print("mocking neopixel")
        import mock_board as board
        import mock_neopixel as neopixel

    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    pixel_pin = board.D18
    
    # The number of NeoPixels
    num_pixels = 50
    
    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    if not mock:
        ORDER = neopixel.RGB
    else:
        ORDER = neopixel.GRB
    
    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )

    logger.info('starting up')
    minutes = 60
    failure_count = 0
    # start in error state
    failure_time_start = time.monotonic() - 11 * minutes 
   
    #for i in range(10):
    while True:

        filename = "/run/shm/image.jpg"
        dog_food = '/run/shm/dog_food'

        
        watchdog_fed = False
        failure_event = False
        if not os.path.exists(dog_food):
            failure_event = True
            logger.debug('dog_food file does not exist')
        # the image file must also exist
        elif not os.path.exists(filename):
            failure_event = True
            logger.debug('image.jpg does not exist')
            # transiently missing?
            # wait till rsync is done?
        else:
            today = datetime.datetime.today()
            modified_date = modification_date(dog_food)
            duration = today - modified_date
            if duration.total_seconds() < 10*minutes:
                watchdog_fed = True
            else:
                failure_event = True
                logger.debug('watchdog not fed')

        if failure_event:
            failure_count += 1
            logger.debug(f'failed {failure_count} times in a row')
            failure_time = time.monotonic() - failure_time_start
            time.sleep(0.100) # to prevent excessive processor usage
        else:
            # reset if we see any good ones
            failure_count = 0
            failure_time = 0
            
        if failure_time > 10*minutes:
            logger.debug(f'failed {failure_count} times in a row, {failure_time} seconds')
                
            # if not fed for more than 10 minutes, go to idle behavior
    
            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((255, 0, 0))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((255, 0, 0, 0))
            pixels.show()
            time.sleep(0.1)
        
            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((0, 255, 0))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((0, 255, 0, 0))
            pixels.show()
            time.sleep(0.1)
        
            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((0, 0, 255))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((0, 0, 255, 0))
            pixels.show()
            time.sleep(0.1)
        
            rainbow_cycle(0.001, num_pixels, ORDER, pixels)  # rainbow cycle with 1ms delay per step
            continue
        
        # extend to read jpg
        
        # https://www.hackster.io/gatoninja236/high-resolution-youtube-player-with-raspberry-pi-d6bdc9
        # https://iotassistant.io/raspberry-pi/writing-to-file-on-ram-disk-on-raspberry-pi/

   
        capture = cv2.VideoCapture()
        try:
            if os.path.exists(filename):
                capture.open(filename)
        except:
            logger.debug("open cv failure")
            continue
    
        success,image = capture.read()
    
        FRAMERATE = 120
    
        while success:
            #img = cv2.resize(image, (num_pixels,num_pixels), interpolation = cv2.INTER_AREA)
            img = cv2.resize(image, (num_pixels,num_pixels), interpolation = cv2.INTER_NEAREST)
            #img = increase_brightness(img)
            #img = apply_brightness_contrast(img, brightness = 0, contrast = 64)
    
            # https://stackoverflow.com/questions/4661557/pil-rotate-image-colors-bgr-rgb
            #image_resized = cv2.cvtColor(image_resized, cv2.COLOR_BRG2RGB)
            #img = img[:,:,::-1]
            img = img[:,:,[2,1,0]]
            display_img = Image.fromarray(img)
            #matrix.SetImage(display_img.convert('RGB'))
            #pixels = display_img.convert('RGB')
            #breakpoint()
    
            #display_img.save("resized.jpg")
            # first row
            for j in range(num_pixels):
                #image_flat = (np.reshape(img[j], -1))
                for i in range(len(pixels)):
                    pixels[i] = img[j][i]
    
                pixels.show()
                #print(pixels)
                time.sleep(0.05)
            #input()
            #time.sleep(1)
            #cv2.imshow('frame',image_resized)
            #time.sleep(1/FRAMERATE)
            success, image = capture.read()
    
        capture.release()
        cv2.destroyAllWindows()
    
    
    if False:
        # extend to read video
        
        # https://www.hackster.io/gatoninja236/high-resolution-youtube-player-with-raspberry-pi-d6bdc9
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        url = "Rick Astley - Never Gonna Give You Up (Official Music Video)-dQw4w9WgXcQ.f137.mp4.part"
        #video = pafy.new(url)
        #best = video.getbest(preftype="mp4")
    
        capture = cv2.VideoCapture()
        capture.open(url)
    
        success,image = capture.read()
    
        FRAMERATE = 120
    
        while success:
            image_resized = cv2.resize(image, (num_pixels,num_pixels), interpolation = cv2.INTER_AREA)
            #image_resized = cv2.cvtColor(image_resized, cv2.COLOR_BRG2RGB)
            display_img = Image.fromarray(image_resized)
            #matrix.SetImage(display_img.convert('RGB'))
            #pixels = display_img.convert('RGB')
            #breakpoint()
            # first row
            image_flat = (np.reshape(image_resized[0], -1))
            for i in range(len(pixels)):
                pixels[i] = image_resized[0][i]
    
    
            pixels.show()
            #time.sleep(1)
            #cv2.imshow('frame',image_resized)
            #time.sleep(1/FRAMERATE)
            success, image = capture.read()
    
        capture.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    import typer
    
#  https://stackoverflow.com/questions/11536764/how-to-fix-attempted-relative-import-in-non-package-even-with-init-py
#    if __package__ is None:
#        import sys
#        from os import path
#        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
#        from components.core import GameLoopEvents
#    else:
#        from ..components.core import GameLoopEvents

    typer.run(main)
    
