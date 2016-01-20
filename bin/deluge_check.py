#!/usr/bin/python

import libtorrent
import os

base_path="/home/bsmith/.config/deluge/state/"
search_path='/home/bsmith/.config/deluge/state/.'

deluge_list = []
fs_list = []
delueg_movie_list = []
fs_movie_list = []

for fn in os.listdir(search_path):
    if ".torrent" in fn:
	p = base_path + fn
	info = libtorrent.torrent_info(p)
	deluge_name = info.name()
    if 'HDTV' in deluge_name:
        deluge_list.append(deluge_name)
    else:
        delueg_movie_list.append(deluge_name)

# BUILD the TV show compare list
comp = os.listdir('/home/bsmith/Downloads/completed/TvShows/')
comp_list = []
for dir in comp:
    comp_list.append(dir)

# build the movies compare list
movie_comp = os.listdir('/home/bsmith/Downloads/completed/Movies/')
movie_comp_list = []
for dir in movie_comp:
    movie_comp_list.append(dir)

# create a list of TVShows to remove
remove_list = []
for torrent in sorted(comp_list):
    if torrent in deluge_list:
        print "torrent in deluge_list       " + torrent
    else:
        remove_list.append(torrent)

# Print out that list
for i in remove_list:
    print "rm -rfv /home/bsmith/Downloads/completed/TvShows/" + i 

# Create a list of Movies to remove
remove_list = []
for torrent in sorted(movie_comp_list):
    if torrent in delueg_movie_list:
        print "torrent in deluge_movie_list " + torrent
    else:
        remove_list.append(torrent)

# print out that list
for i in remove_list:
    print "rm -rfv /home/bsmith/Downloads/completed/Movies/" + i


        


