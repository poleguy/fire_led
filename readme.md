to copy to raspberry pi:
rsync -rahP ./ pi@fire.local:/home/pi/fire_led/

to run
add to rc.local and boot
or run 
python test_mock_neopixel.py
