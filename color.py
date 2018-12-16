from PIL import Image, ImageFilter
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import json, operator

# close enough for now
lab_def_colors = {
    "red": { 'l': 5140.11747498726, 'a': 5854.540388686413, 'b': 4703.999578781808 },
    "orange": { 'l': 6808.631086548932, 'a': 1570.9044095408976, 'b': 5774.29818155228 },
    "yellow": { 'l': 8359.6222362322, 'a': -1587.0267095039594, 'b': 6911.928415647229 },
    "green": { 'l': 4412.98556365553, 'a': -3650.8864478376727, 'b': 3505.0619996219075 },
    "blue": { 'l': 3440.99427865288, 'a': 4877.356355591926, 'b': -8151.7744794282125 },
    "indigo": { 'l': 2599.7405512221367, 'a': 3626.1956224077812, 'b': -3778.207207219171 },
    "violet": { 'l': 6765.249743889395, 'a': 4977.408694893711, 'b': -3226.7699841644912 },
    "brown": { 'l': 4029.7637431690864, 'a': 2340.1675308635104, 'b': 3428.617408173726 },
    "black": { 'l': 1207.5848657907516, 'a': -0.004845706917500081, 'b': -0.09030751501910572 },
    "white": { 'l': 8600.309785328083, 'a': -0.03412277570191691, 'b': -0.6359326166119672 },
    "grey": { 'l': 5376.289444627731, 'a': -0.02135483610388178, 'b': -0.39798159786101905 }
}


def blur_and_resize( image ):
    image = Image.open( image, 'r' )
    image = image.convert( 'RGB' )
    image = image.filter( ImageFilter.GaussianBlur( 30 ) )
    image = image.resize( (150, 150) )
    result = image.convert( 'P', palette = Image.ADAPTIVE, colors = 20 )
    result.putalpha( 0 )
    return result


def luminance( r, g, b ):
    return 0.299 * r + 0.587 * g + 0.114 * b


def check_against_dict( i, dt ):
    t = 0
    for item in dt:
        s = json.loads( dt[ item ] )
        if abs( i - s[ 'luminance' ] ) > 100:
            t += 1
    if t == len( dt ):
        return True
    return False


def get_colors( image_path ):
    try:
        modified_image = blur_and_resize( image_path )

        color_dict = { }
        y = 0
        results = { }

        for co in modified_image.getcolors( (150 * 150) ):
            l = luminance( co[ 1 ][ 0 ], co[ 1 ][ 1 ], co[ 1 ][ 2 ] )
            if check_against_dict( l, color_dict ):
                color_dict[ y ] = json.dumps(
                    { 'luminance': l, 'rgb': { 'red': co[ 1 ][ 0 ], 'green': co[ 1 ][ 1 ], 'blue': co[ 1 ][ 2 ] } } )
                for h in lab_def_colors:
                    c = json.loads( color_dict[ y ] )[ 'rgb' ]
                    lab = convert_color( sRGBColor( c[ 'red' ], c[ 'green' ], c[ 'blue' ] ), LabColor )
                    delta_e = delta_e_cie2000(
                        LabColor( lab_def_colors[ h ][ 'l' ], lab_def_colors[ h ][ 'a' ], lab_def_colors[ h ][ 'b' ] ),
                        lab )
                    if results.get( h ) is None or delta_e < results[ h ]:
                        results[ h ] = delta_e
                y += 1

        return sorted( results.items(), key = lambda x: x[ 1 ] )
    except Exception as e:
        print( e )
