#!/bin/bash

echo -n "/home/bsmith/repos/flexget_files/bin/torrent_complete.py $1 $2 ${3}/ && " >> /home/bsmith/logs/tor_comp/deluge_call.log
python /home/bsmith/repos/flexget_files/bin/torrent_complete.py $1 $2 ${3} 
#D=`date +%m-%d-%y_%H:%M:%S`
#echo -n "/home/bsmith/repos/flexget_files/bin/torrent_complete.py $1 $2 ${3}/ && " >> /home/bsmith/logs/tor_comp/deluge_call.log

