# setup host controller  pc running check_calendar code
sudo cp led_controller.service /lib/systemd/system/led_controller.service
sudo systemctl daemon-reload
sudo systemctl enable led_controller.service
sudo systemctl start led_controller.service
