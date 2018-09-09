#!/bin/sh

while :
do
wget -N https://data.val.se/val/val2018/valnatt/valnatt.zip 
unzip -o valnatt.zip -d valnatt
rm -r valnatt.zip 
sleep 30s
done 
