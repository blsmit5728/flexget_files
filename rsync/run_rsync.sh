#!/bin/bash

DATE=`date +%m_%d_%Y` 
LOG_PATH="/home/bsmith/.flexget/rsync/rsync_logs/"

rsync -arv --ignore-existing --stats /mnt/disk1/Library/ /mnt/disk2/Library/ >> $LOG_PATH/rsync_log_$DATE.log
#rsync -arv --ignore-existing --stats /mnt/disk1/Library/ /mnt/disk3/Library/ >> $LOG_PATH/disk3_rsync_log_$DATE.log

