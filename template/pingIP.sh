#!/bin/bash

for siteip in $(seq 1 254)
do
    site="192.168.130.${siteip}"
    ping -c2  ${site} &> /dev/null
    if [ "$?" == "0" ]; then
        echo "$site is up" >> pingfile
    else
        echo "$site is down"
    fi  
done
