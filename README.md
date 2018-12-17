# imagetag
tag images with basic info
  - dominant color
  - tags added by picasa and windows
  - file modified date
 
intended for use with Hydrus https://github.com/hydrusnetwork/hydrus

## flags
```
[ -i --input-path ]          set the input path (default is the current directory)
[ -o --output-path ]         set the output path (default is the current directory)

[ -f --force ]               will overwrite existing text files accompanying the images
[ -c --copy ]                copy to output directory (if supplied) instead of moving
[ -x --extract-tags-only]    only fetch tags within the image metadata, no modified date or colors
```

## examples

*only extract tags from image metadata, move to output directory*
```
python3 main.py -x -i "D:\example\dir\ecto\ry" -o "D:\example\dir\ecto\ry\New Folder (1)"
```