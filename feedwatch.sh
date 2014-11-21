#!/bin/bash
#source /home/pi/.bashrc
cd /home/pi/uncoolstars
python -c 'import getData; getData.addFromFeed()' &>> feedwatch.log
echo `date` &>> feedwatch.log
