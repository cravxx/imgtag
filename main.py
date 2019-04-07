import os
import shutil
import time
import argparse
import hashlib

from fnmatch import fnmatch
from datetime import datetime
from pathlib import Path
from loguru import logger

from PathType import PathType
from color import get_colors
from file_tags import get_tags

color_exclude_list = [ "*.webm", "*.mp4", "*.gif", "*.gifv", "*.mov", "*.avi" ]
include_list = [ "*.webm", "*.mp4", "*.gif", "*.gifv", "*.jpg", "*.jpeg", "*.png", "*.webp", "*.jpeg_large",
                 "*.jpg_large", "*.mov", "*.avi" ]


parser = argparse.ArgumentParser( description = 'image processor / sorter' )
parser.add_argument( '-i', '--input-path', type = PathType( exists = True, type = 'dir' ),
                     help = "set the input path (default is the current directory)" )
parser.add_argument( '-o', '--output-path', type = PathType( exists = True, type = 'dir' ),
                     help = "set the output path (default is the current directory)" )

parser.add_argument( '-c', '--copy', action = "store_true",
                     help = "copy to output directory (if supplied) instead of moving" )
parser.add_argument( '-g', '--get-colors', action = "store_true",
                     help = "calculate image color" )
parser.add_argument( '-m', '--get-metadata', action = "store_true",
                     help = "get image exif metadata" )
parser.add_argument( '-f', '--get-file-info', action = "store_true",
                     help = "get file info" )

args = parser.parse_args()

_INPUT_DIR = os.getcwd() if args.input_path is None else args.input_path
# default is same directory as input
_OUTPUT_DIR = args.input_path if args.output_path is None else args.output_path


def write_tag( file, namespace = "", tag = "" ):
    file.write( (namespace + (":" if tag != "" else "") + str( tag ) + os.linesep).encode( "utf_8" ) )


if __name__ == "__main__":

    for dirpath, dirnames, filenames in os.walk( _INPUT_DIR ):
        for matched_file in [ f for f in filenames if any( fnmatch( f, pattern ) for pattern in include_list ) ]:
            try:
                unique_filename = hashlib.sha224( str( time.time() ).encode() ).hexdigest() + matched_file[
                                                                                              matched_file.rindex(
                                                                                                  "." ): ].replace(
                    ".jpg_large", ".jpg" )

                text_file_path = Path( os.path.join( _OUTPUT_DIR, unique_filename ) + ".txt" )

                with open( text_file_path, "wb" ) as text_file:

                    # windows and picasa tags
                    if args.get_metadata:
                        try:
                            metadata_tags = get_tags( os.path.join( dirpath, matched_file ) )
                            if metadata_tags is not None:
                                for k in metadata_tags:
                                    for v in metadata_tags[ k ]:
                                        logger.opt( ansi = True ).info(
                                            "[ <red> {0} </red> ] {1}: {2}".format( matched_file, k, v ) )
                                        write_tag( text_file, k, v )
                        except Exception as err:
                            pass

                    # colors
                    if args.get_colors:
                        if not any( fnmatch( matched_file, pattern ) for pattern in color_exclude_list ):
                            image_colors = get_colors( os.path.join( dirpath, matched_file ) )
                            if image_colors is not None:
                                # pick first two
                                logger.opt( ansi = True ).info( "[ <red> {} </red> ] matched colors: {} {}",
                                                                matched_file,
                                                                image_colors[ 0 ][ 0 ], image_colors[ 1 ][ 0 ] )
                                write_tag( text_file, "color", image_colors[ 0 ][ 0 ] )
                                write_tag( text_file, "color", image_colors[ 1 ][ 0 ] )

                    # file info
                    if args.get_file_info:
                        write_tag( text_file, "filename", matched_file[ :matched_file.rindex( "." ) ] )

                        d = datetime.strptime(
                            time.ctime( os.path.getmtime( os.path.join( dirpath, matched_file ) ) ),
                            "%a %b %d %H:%M:%S %Y" )
                        write_tag( text_file, "modified", d.strftime( '%Y/%m/%d %H:%M:%S' ) )
                        write_tag( text_file, "month", d.strftime( '%B' ) )
                        write_tag( text_file, "year", d.strftime( '%Y' ) )

                        logger.opt( ansi = True ).info( "[ <red> {} </red> ] modified: {}", matched_file,
                                                        d.strftime( '%Y/%m/%d %H:%M:%S' ) )

                    if (_INPUT_DIR != _OUTPUT_DIR):
                        try:
                            if args.copy:
                                logger.opt( ansi = True ).info( "[ <red> {} </red> ] copied to: {}", matched_file,
                                                                os.path.join( _OUTPUT_DIR, unique_filename ) )
                                shutil.copy( os.path.join( dirpath, matched_file ),
                                             os.path.join( _OUTPUT_DIR, unique_filename ) )
                            else:
                                logger.opt( ansi = True ).info( "[ <red> {} </red> ] moved to: {}", matched_file,
                                                                os.path.join( _OUTPUT_DIR, unique_filename ) )
                                shutil.move( os.path.join( dirpath, matched_file ),
                                             os.path.join( _OUTPUT_DIR, unique_filename ) )
                        except Exception as err:
                            logger.error( err )

            except Exception as err:
                logger.error( err )
