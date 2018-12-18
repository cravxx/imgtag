# imgtag
tag images with basic info
  - dominant color
  - tags added by picasa and windows
  - metadata such as title, creator, copyright and ratings
  - file modified date
 
intended for use with Hydrus https://github.com/hydrusnetwork/hydrus

## usage
```
[ -i --input-path ]          set the input path (default is the current directory)
[ -o --output-path ]         set the output path (default is same as input)

[ -f --force ]               will overwrite existing text files accompanying the images
[ -c --copy ]                copy to output directory (if supplied) instead of moving
[ -x --extract-tags-only]    only fetch tags within the image metadata, no modified date or colors
```

*only extract tags from image metadata, move to output directory*
```
python3 main.py -x -i "D:\example\dir\ecto\ry" -o "D:\example\dir\ecto\ry\New Folder (1)"
```