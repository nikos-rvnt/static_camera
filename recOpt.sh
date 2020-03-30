#!/bin/bash

STREAM="rtsp://192.168.2.233:8554/video0"
FILE="staticOptical__"
TIME=$1 # in 00:00:00 format
OUT=$FILE`date '+%m-%d-%y_%H_%M'`
CWD=/home/theasis/Videos
DATE=`date '+%m-%d-%y'`

if [ ! -d $CWD/streams ]
then
 mkdir -p $CWD/streams
fi

ffmpeg -i $STREAM -c copy -an $CWD/streams/$OUT.mp4

if [ ! -d $CWD/recordings/$DATE ]
then
 mkdir -p $CWD/recordings/$DATE
fi

mv $CWD/streams/$OUT.mp4 $CWD/recordings/$DATE/$OUT.mp4

 
