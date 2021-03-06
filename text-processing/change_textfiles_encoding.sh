#!/bin/bash
#enter input encoding here
FROM_ENCODING="iso-8859-1"
#output encoding(UTF-8)
TO_ENCODING="UTF-8"
CONVERT=" iconv  -f   $FROM_ENCODING  -t   $TO_ENCODING"
#loop to convert multiple files 
for  file  in  *.txt; do
     $CONVERT   "$file"   -o  "${file%.txt}"
done
exit 0