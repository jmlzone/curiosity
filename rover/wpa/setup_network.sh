#!/bin/bash
echo "----------------------------------------------------------------------"
echo "setup networking"
cd ~
sudo cp ~/curiosity/rover/wpa/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
sudo chmod 600  /etc/wpa_supplicant/wpa_supplicant.conf
echo "----------------------------------------------------------------------"
