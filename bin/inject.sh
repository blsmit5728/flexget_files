#!/bin/bash

flexget --task=tv-shows --inject "$1" "http://uranium.local:48880/torrentleech/$1.torrent"
