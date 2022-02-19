#! /bin/sh
apt update
apt -y install acpid
/bin/cp button_power /etc/acpi/events
systemctl restart acpid
systemctl enable acpid
