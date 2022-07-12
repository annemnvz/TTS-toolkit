#!/bin/sh

# Will find all wav files in $source directory
# Process them and substitute the original audios
source=""

find $source -type f -name "*.wav" -print | while IFS= read -r file;
do
   out="${file}_new.wav"  # temp file
   sox -S "$file" -r 22050 -c 1 "$out"  # change to 16-bits
   rm $file
   mv $out $file
done