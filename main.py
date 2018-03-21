import json, sys, glob, os, shutil, operator, time
from os import path
from colour import Color
from fnmatch import fnmatch
from datetime import datetime
from util import write_tag
from color import get_colors
from file_tags import get_tags

color_exclude_list = [ "*.webm", "*.mp4", "*.gif", "*.gifv" ]

_DIR = os.getcwd() #"image"

for matched_file in [f for f in os.listdir(_DIR) if not fnmatch(f, "*.txt")]:
    try:
        with open(os.path.join(_DIR, matched_file) + ".txt", "wb") as text_file:
            
            #colors
            if not any(fnmatch(matched_file, pattern) for pattern in color_exclude_list):
                image_colors = get_colors(os.path.join(_DIR, matched_file))
                if image_colors is not None:
                    #pick first two
                    print("[",matched_file,"] matched colors: ",image_colors[0][0],image_colors[1][0])
                    write_tag(text_file, "color", image_colors[0][0])
                    write_tag(text_file, "color", image_colors[1][0])

            #windows tags
            meta_tags = get_tags(os.path.join(_DIR, matched_file))
            if meta_tags is not None:
                for tag in meta_tags:
                    write_tag(text_file, "metatag", tag.decode('utf-8'))

            d = datetime.strptime(time.ctime(os.path.getmtime(os.path.join(_DIR, matched_file))),"%a %b %d %H:%M:%S %Y")
            write_tag(text_file, "modified", d.strftime('%Y/%m/%d %H:%M:%S'))
            write_tag(text_file, "year", d.strftime('%Y'))
            print("[",matched_file,"] modified: ",d.strftime('%Y/%m/%d %H:%M:%S'))

    except Exception as e:
        print(e)