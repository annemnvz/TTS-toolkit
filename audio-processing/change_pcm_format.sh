#!/bin/sh

# Will find all wav files in $source directory
# Process them and substitute the original audios

source=""

find $source -type f -name "*.wav" -print | while IFS= read -r file;
do
   out="${file}_16bit.wav" # temp file
   sox -S "$file" -b 16 "$out" # change to 16-bits
   rm $file
   mv $out $file
done