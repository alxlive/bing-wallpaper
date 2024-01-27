#!/bin/bash

DIR=/Users/alxlive/projects/xfce-bing-wallpaper/
cd $DIR
echo `date` > logs.txt
python3 bing-wallpaper.py >> logs.txt
