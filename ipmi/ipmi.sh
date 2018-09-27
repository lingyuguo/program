#!/bin/bash
IPMI_IP = "192.168.255.254"
IPMI_USER = "ADMIN"
IPMI_PASSWD = "11111111"
ipmitool -H $IPMI_IP -U $IPMI_USER -P $IPMI_PASSWD -I lan chassis status > chassis.txt
ipmitool -H $IPMI_IP -U $IPMI_USER -P $IPMI_PASSWD -I lan sendors list   > sendors.txt
