#!/usr/bin/env bash

ALL_PIDS=$(wmic process get processid,commandline | grep python.exe | awk '{printf "//pid %s ",$NF}')
if [ "$ALL_PIDS" != "" ]
then
        taskkill -f $ALL_PIDS
fi