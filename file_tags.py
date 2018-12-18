import re

from lxml import etree

_NAMESPACES = { 'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'xmp': 'http://ns.adobe.com/xap/1.0/',
                'dc': 'http://purl.org/dc/elements/1.1/',
                'x': 'adobe:ns:meta/' }


# works for both windows and picasa
def get_tags( matched_file ):
    x_packet = get_packet( matched_file )
    if x_packet is not None:
        return [ t.text for t in x_packet.iterfind( ".//rdf:li", _NAMESPACES ) ]
    else:
        return [ ]


def get_packet( matched_file ):
    with open( matched_file, "rb" ) as imageFile:
        x_packet = re.search( b'(<\?xpacket.+begin.+>.*?<\?xpacket.+end.+>)', imageFile.read() )
        if x_packet is not None:
            return etree.fromstring( x_packet.group(), etree.XMLParser( ns_clean = True ) )
        else:
            return None
