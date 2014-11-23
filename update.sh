#!/bin/bash
echo ---------------------------------------------------------- &>> update.log
echo "Updating data" `date` &>> update.log
cd ~/uncoolstars
python updatedata.py &>> update.log
echo "Successfully updated" `date` &>> update.log
cd -
