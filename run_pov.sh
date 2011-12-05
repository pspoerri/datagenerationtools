#!/bin/bash
for i in ls *.pov
do 
    povray $i +W1920 +H1200 -d
#    povray $i +W800 +H600 -d 
done
