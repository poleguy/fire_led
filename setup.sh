sudo pip install opencv-python
sudo pip install rpi_ws281x adafruit-circuitpython-neopixel
sudo pip install adafruit-blinka
sudo pip install pyyaml pygame
sudo pip install typer

sudo cp led.service /lib/systemd/system/led.service
sudo systemctl daemon-reload
sudo systemctl enable led.service
sudo systemctl start led.service
#sudo reboot
