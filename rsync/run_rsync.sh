#!/bin/bash

DATE=`date +%m_%d_%Y` 
LOG_PATH="/home/bsmith/.flexget/rsync/rsync_logs/"

LIST="GoPro Home_Movies Music Pictures Stuff TvShows Video Workout"

for i in $LIST
do
     rsync -arvh --ignore-existing --stats /mnt/disk1/Library/$i/* /mnt/disk2/Library/$i/ >> $LOG_PATH/rsync_${i}_log_${DATE}.log
done

rsync -arvh --ignore-existing --stats /mnt/disk1/Library/Movies/* /mnt/disk3/Library/Movies/ >> $LOG_PATH/rsync_Movies_log_$DATE.log

