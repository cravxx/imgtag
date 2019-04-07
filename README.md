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

[ -c --copy ]                copy to output directory (if supplied) instead of moving
[ -m --get-metadata ]        get image exif metadata and windows tags
[ -g --get-color ]           calculate image color
[ -f --get-file-info ]       get filename and date modified
```

*get metadata and file info, then move to output directory*
```
python3 main.py -m -f -i "D:\example\dir\ecto\ry" -o "D:\example\dir\ecto\ry\New Folder (1)"
```