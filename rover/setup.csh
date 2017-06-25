#
# copyleft 2016 James Lee jml@jmlzone.com
# This file is one of many created by or found by James Lee
# <jml@jmlzone.com> to help with the new horizon model for stellafane 2016.
#
# All the original files are CopyLeft 2016 James Lee permission is here
# by given to use these files for educational and non-commercial use.
# For commercial or other use please contact the author as indicated in
# the file or jml@jmlzone.com
#
#!/bin/csh
# This script will update the Stellafane New Horizon software
#
# copyleft 2016 James Lee jml@jmlzone.com
# This file is one of many created by or found by James Lee
# <jml@jmlzone.com> to help with the new horizon model for stellafane 2016.
#
# All the original files are CopyLeft 2016 James Lee permission is here
# by given to use these files for educational and non-commercial use.
# For commercial or other use please contact the author as indicated in
# the file or jml@jmlzone.com
echo "----------------------------------------------------------------------"
echo "Updating html"
sudo cp html/* /var/www/html
sudo chmod a+r /var/www/html/*
echo "----------------------------------------------------------------------"
echo "Updating cgi-bin"
sudo cp cgi-bin/* /usr/lib/cgi-bin
sudo chmod a+rx /usr/lib/cgi-bin/*
sudo mkdir -p /var/www/html/curiosity/missions    
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "all_done"
