#!/bin/bash

dir="assets/images/tiles/brick"

find "$dir" -type f -name '*.png' -print0 |
while IFS= read -r -d $'\0' file; do
    filename=$(basename -- "$file")
    filename_no_ext="${filename%.*}"

    magick convert "$file" -resize 16x16 "$dir/${filename_no_ext}.png"

    echo "Resized: $file"
done