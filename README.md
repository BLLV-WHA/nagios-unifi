# Nagios Unifi Plugin

rename config_example.py to config.py

modify config.py to your needs

```
usage: check_unifi.py [-h] --hostname HOSTNAME --metric {status,cpu,memory,speed,satisfaction,temperature,overheating,power_level} --controller_host CONTROLLER_HOST --controller_user CONTROLLER_USER --controller_password CONTROLLER_PASSWORD [-w WARNING] [-c CRITICAL]

optional arguments:
  -h, --help            show this help message and exit
  --hostname HOSTNAME   name of the unifi device
  --metric {status,cpu,memory,speed,satisfaction,temperature,overheating,power_level}
                        metric to be measured
  --controller_host CONTROLLER_HOST
                        address of unifi controller
  --controller_user CONTROLLER_USER
                        login user for the controller
  --controller_password CONTROLLER_PASSWORD
                        password for the controller
  -w WARNING, --warning WARNING
  -c CRITICAL, --critical CRITICAL

```
