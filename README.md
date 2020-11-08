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

## Metrics

### status
Type: boolean

Overall status reported by the device.

### cpu
Type: float [0 - 100]

Ourrent cpu usage of the device.

### memory
Type: float [0 - 100]

Current memory usage of the device.

### speed
Type: int [0 - 1000]

Current network connection speed of the device.

### satisfaction
Type: int [0 - 100]

Overall user experience of all clients of the device.
If no clients are detected a satisfaction of 100 is assumed.

### temperature
Type: float

The temperatur of the device in C.

### temperature
Type: boolean

Overheating reported by the device.

### temperature
Type: float [0 - 100]

Percent value of the powerusage if the device.
Calculated of the reported max power and the per port used power.
