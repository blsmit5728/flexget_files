#!/bin/bash

HD_DIR="XBMC_LIBRARY"
FS=25 #min freespace

FLEXGET_LOG="/home/bsmith/.flexget/flexget-copy-sorting.log"
FLEXGET_CONFIG="/home/bsmith/.flexget/copy_sort.yml"
FLEXGET_TV_TASK="sort_copied_tv_shows"

TV_STAGING_DIR="/media/300GB/$HD_DIR/staged/tvshows/"

RSYNC_FILE="/home/bsmith/.flexget/rsync/rsync_logs/rsync_log_`date +%m_%d_%Y`.log"


#test to see if the drive is present
df -h | grep 300GB
if [ $? -eq "0" ]
then
    #the drive is there, we know what the directory is.
    cd /media/300GB/$HD_DIR/
else
    #the drive is not here...
    exit
fi

# Check the space on the backup drive...
FREE=`df -h | grep 300GB | awk '{ print $4 "\t" }' | cut -d'G' -f1`
if [ "$FREE" -lt "$FS" ]
then
    echo "Not enough Free Space on /media/300GB/$HD_DIR/ to copy New Data"
    exit
fi

# flexget copy_sort.yml deletes this dir every time...
#mkdir $TV_STAGING_DIR

# Get list of recently added Videos from the daily .rsync log file

#tail -n60  /home/bsmith/.rsync_log.log | grep ".mkv"| grep "TvShows" | while read -r line  
#cat /home/bsmith/.rsync_log.log | grep .mkv | grep TvShows | while read -r line
cat $RSYNC_FILE | grep .mkv | grep TvShows | while read -r line
do 
    #echo "/mnt/disk1/Library/$line" 
    cp -v "/mnt/disk1/Library/$line" $TV_STAGING_DIR
done

flexget --logfile $FLEXGET_LOG -c $FLEXGET_CONFIG  --task $FLEXGET_TV_TASK --disable-advancement

