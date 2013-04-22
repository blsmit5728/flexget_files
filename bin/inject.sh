#!/bin/bash

flexget --task=tv-shows --inject "$1" "http://www.brandonleesmith.us:48880/torrentleech/$1.torrent"
