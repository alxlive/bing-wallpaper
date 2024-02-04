#!/bin/bash

DIR=/Users/alxlive/projects/bing-wallpaper/
cd $DIR
echo `date` > logs.txt
if [ -f /usr/local/bin/python3 ]; then
    echo "Using /usr/local/bin/python3" >> logs.txt
    PYTHON3=/usr/local/bin/python3
else
    echo "Falling back to `which python3`" >> logs.txt
    PYTHON3=python3
fi

$PYTHON3 bing-wallpaper.py >> logs.txt

title=`tail -1 logs.txt | sed 's/Title: //'`
oldtitle=`cat title.txt`

if [ "$title" != "$oldtitle" ] ; then
    echo "$title" > title.txt
    echo "overwrote title file"
fi
