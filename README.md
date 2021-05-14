# linux_fan_control

## Setup
```
sudo cp fancontrol.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start fancontrol.service
```
##To enable on startup
```
sudo systemctl enable fancontrol.service
```
