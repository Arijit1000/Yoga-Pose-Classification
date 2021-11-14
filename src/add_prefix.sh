#!/bin/bash
#for file in *.jpg;do cp $file "$1_$file";done
for file in *.png;do cp $file "$1_$file";done

#how to add prefixes
#for dir in `ls|fgrep -v zip`;do cd $dir;bash ~/proj/capstone/scripts/add_prefix.sh google;cd ..;done

#hwo to move prefixed files to interim dir
#for dir in `ls`;do mv ../youtube_yoga_frames/$dir/youtube* $dir/.;done
