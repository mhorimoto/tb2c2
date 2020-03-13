#! /bin/sh
#set -x

/usr/local/bin/writelcd.py "System is" 1 i
/usr/local/bin/writelcd.py "    shutdown" 2 n
echo 0 > /sys/class/leds/orangepi\:green\:pwr/brightness
