import os
import shutil
import time
import argparse

from fnmatch import fnmatch
from datetime import datetime
from pathlib import Path
from loguru import logger

from PathType import PathType
from color import get_colors
from file_tags import get_tags, get_packet

color_exclude_list = [ "*.webm", "*.mp4", "*.gif", "*.gifv" ]
include_list = [ "*.webm", "*.mp4", "*.gif", "*.gifv", "*.jpg", "*.jpeg", "*.png" ]

parser = argparse.ArgumentParser( description = 'image processor / sorter' )
parser.add_argument( '-i', '--input-path', type = PathType( exists = True, type = 'dir' ),
                     help = "set the input path (default is the current directory)" )
parser.add_argument( '-o', '--output-path', type = PathType( exists = True, type = 'dir' ),
                     help = "set the output path (default is the current directory)" )

parser.add_argument( '-f', '--force', action = "store_true",
                     help = "will overwrite existing text files accompanying the images" )
parser.add_argument( '-c', '--copy', action = "store_true",
                     help = "copy to output directory (if supplied) instead of moving" )
parser.add_argument( '-x', '--extract-tags-only', action = "store_true",
                     help = "only fetch tags within the image metadata, no modified date or colors" )

args = parser.parse_args()

_INPUT_DIR = os.getcwd() if args.input_path is None else args.input_path
# default is same directory as input
_OUTPUT_DIR = args.input_path if args.output_path is None else args.output_path


def write_tag( file, namespace = "", tag = "" ):
    file.write( (namespace + (":" if tag != "" else "") + str( tag ) + os.linesep).encode( "utf_8" ) )


if __name__ == "__main__":

    for matched_file in [ f for f in os.listdir( _INPUT_DIR ) if
                          any( fnmatch( f, pattern ) for pattern in include_list ) ]:
        try:
            text_file_path = Path( os.path.join( _OUTPUT_DIR, matched_file ) + ".txt" )

            if text_file_path.exists() == False or text_file_path.exists() and args.force:

                with open( text_file_path, "wb" ) as text_file:

                    # windows and picasa tags
                    metadata_tags = get_tags( os.path.join( _INPUT_DIR, matched_file ) )
                    if metadata_tags is not None:
                        print( metadata_tags )
                        for tag in metadata_tags:
                            logger.opt( ansi = True ).info( "[ <red> {} </red> ] metatag: {}", matched_file, tag )
                            write_tag( text_file, "metatag", tag )


                    if not args.extract_tags_only:

                        # colors
                        if not any( fnmatch( matched_file, pattern ) for pattern in color_exclude_list ):
                            image_colors = get_colors( os.path.join( _INPUT_DIR, matched_file ) )
                            if image_colors is not None:
                                # pick first two
                                logger.opt( ansi = True ).info( "[ <red> {} </red> ] matched colors: {} {}",
                                                                matched_file,
                                                                image_colors[ 0 ][ 0 ], image_colors[ 1 ][ 0 ] )
                                write_tag( text_file, "color", image_colors[ 0 ][ 0 ] )
                                write_tag( text_file, "color", image_colors[ 1 ][ 0 ] )

                        # modified time
                        d = datetime.strptime(
                            time.ctime( os.path.getmtime( os.path.join( _INPUT_DIR, matched_file ) ) ),
                            "%a %b %d %H:%M:%S %Y" )
                        write_tag( text_file, "modified", d.strftime( '%Y/%m/%d %H:%M:%S' ) )
                        write_tag( text_file, "year", d.strftime( '%Y' ) )

                        logger.opt( ansi = True ).info( "[ <red> {} </red> ] modified: {}", matched_file,
                                                        d.strftime( '%Y/%m/%d %H:%M:%S' ) )

                    if (_INPUT_DIR != _OUTPUT_DIR):
                        try:
                            if args.copy:
                                logger.opt( ansi = True ).info( "[ <red> {} </red> ] copied to: {}", matched_file,
                                                                _OUTPUT_DIR )
                                shutil.copy( os.path.join( _INPUT_DIR, matched_file ),
                                             os.path.join( _OUTPUT_DIR, matched_file ) )
                            else:
                                logger.opt( ansi = True ).info( "[ <red> {} </red> ] moved to: {}", matched_file,
                                                                _OUTPUT_DIR )
                                shutil.move( os.path.join( _INPUT_DIR, matched_file ),
                                             os.path.join( _OUTPUT_DIR, matched_file ) )
                        except Exception as err:
                            logger.error( err )

            else:
                logger.opt( ansi = True ).info(
                    "[ <red> {} </red> ] was skipped because a .txt file already exists. Rerun with the <green>-f --force</green> flag to process anyway",
                    matched_file )

        except Exception as err:
            logger.error( err )
