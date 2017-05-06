#!/bin/sh
#
# copies files from here where they were gotten from git and puts them where they need to be on the system
# please sudo this file!
#
echo "----------------------------------------------------------------------"
echo "Updating html"
sudo cp html/* /var/www/html
sudo chmod a+r /var/www/html/*
echo "----------------------------------------------------------------------"
echo "Updating cgi-bin"
sudo cp cgi-bin/* /usr/lib/cgi-bin
sudo chmod a+rx /usr/lib/cgi-bin/*
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "all_done"
