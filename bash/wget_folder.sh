#!/usr/bin/env bash
# wget_folder <uri> <user> <pass> [<cur-dirs>]
wget -r -np -nH -cur-dirs=${4:-3} -R index.html* $1 --user=$2 --password=$3