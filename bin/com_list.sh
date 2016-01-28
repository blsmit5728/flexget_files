#!/bin/bash

SORT_FILE="/home/bsmith/.flexget/.sort-lock"
CONFIG_FILE="/home/bsmith/.flexget/.config-lock"
DELUGE_FILE="/home/bsmith/logs/tor_comp/deluge_call.log"
LOG_FILE="/home/bsmith/logs/tor_comp/sort.log"
LOCK_FILE="/tmp/com_lock"

if [ -e $LOCK_FILE ]
then
    exit
fi

if [ -e $SORT_FILE ]
then
    exit
fi

if [ -e $CONFIG_FILE ]
then
    exit
fi

if [ -e $DELUGE_FILE ]
then
    echo "Deluge file there"
else
    exit
fi

touch $LOCK_FILE
while IFS='' read -r line || [[ -n "$line" ]];
do
    #echo $line | awk '{print $1}'
    #echo $line | awk '{print $2}'
    A=`echo $line | awk '{print $1}'`
    B=`echo $line | awk '{print $2}'`
    C=`echo $line | awk '{print $3}'`
    echo "PROCESSING: /home/bsmith/repos/flexget_files/bin/torrent_complete.py $A $B $C" >> $LOG_FILE
    /home/bsmith/repos/flexget_files/bin/torrent_complete.py $A $B $C
done < "$DELUGE_FILE"
rm -rf $LOCK_FILE
rm -rf $DELUGE_FILE

