import re

from lxml import etree

_NAMESPACES = { 'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'xmp': 'http://ns.adobe.com/xap/1.0/',
                'dc': 'http://purl.org/dc/elements/1.1/',
                'x': 'adobe:ns:meta/',

                #microsoft
                'MicrosoftPhoto': 'http://ns.microsoft.com/photo/1.0/' }


def get_tags( matched_file ):
    tags = { }
    x_packet = get_packet( matched_file )
    if x_packet is not None:

        #windows Title
        title = x_packet.iterfind( ".//dc:title/rdf:Alt/rdf:li", _NAMESPACES )
        tags[ "title" ] = [ title_el.text for title_el in title if title_el is not None ]

        # xmp Tags
        # there's also two MicrosoftPhoto tag collections, MicrosoftPhoto:LastKeywordIPTC and
        # MicrosoftPhoto:LastKeywordXMP, but from what i can tell they always get copied to
        # dc:subject so there's not much use checking them
        title = x_packet.iterfind( ".//dc:subject/rdf:Bag/rdf:li", _NAMESPACES )
        tags[ "tags" ] = [ title_el.text for title_el in title if title_el is not None ]

        # windows Rating
        title = x_packet.iterfind( ".//MicrosoftPhoto:Rating", _NAMESPACES )
        tags[ "rating" ] = [ title_el.text for title_el in title if title_el is not None ]

        #xmp Rating
        title = x_packet.iterfind( ".//xmp:Rating", _NAMESPACES )
        tags[ "stars" ] = [ title_el.text for title_el in title if title_el is not None ]

        # windows Creators
        title = x_packet.iterfind( ".//dc:creator/rdf:Seq/rdf:li", _NAMESPACES )
        tags[ "creator" ] = [ title_el.text for title_el in title if title_el is not None ]

        # windows Copyrights
        title = x_packet.iterfind( ".//dc:rights/rdf:Alt/rdf:li", _NAMESPACES )
        tags[ "copyright" ] = [ title_el.text for title_el in title if title_el is not None ]

    return tags


def get_packet( matched_file ):
    with open( matched_file, "rb" ) as imageFile:
        x_packet = re.search( b'(?s)(<\?xpacket.+begin.+>.*<\?xpacket.+end.*?>)', imageFile.read() )
        if x_packet is not None:
            st = x_packet.group()
            st = re.sub(b'\s+', b' ', st)
            return etree.fromstring( st , etree.XMLParser( ns_clean = True, remove_blank_text=True) )
        else:
            return None
