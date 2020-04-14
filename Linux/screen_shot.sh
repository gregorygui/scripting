#!/usr/bin/bash
I=0
while [ 1 ]; do
#change /path/to/where/svae/screenshots to your path 
FILENAME=/path/to/where/save/screenshots/${BASENAME}${I}.png
echo "Saving ${FILENAME}"
import -window root -silent ${FILENAME}
I=$[ $I + 1 ]
#change time to how often take screenshot (5)
sleep 5
done
