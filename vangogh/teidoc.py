from collections import defaultdict
import io
from lxml import etree
import os.path
import re
import unicodedata

import langdetect
import xmltodict

from .utils import flatten_dict


class TeiDocument:
    """This class represents a TEI-document

    Parameters
    ----------
    xml:
        either a path to an xml-file or a fileobject that has a read()-method
    parser:
        An instance of an etree.XMLParser.
    """

    def __init__(self, xml, parser=etree.XMLParser()):
        try:
            self.xml = etree.fromstring(xml, parser)
        except etree.XMLSyntaxError:
            if os.path.exists(xml):
                self.xml = etree.parse(xml, parser)
            else:
                raise ValueError(f"Can't parse data: {xml}")

        self.nsmap = self._get_nsmap()

    def _get_nsmap(self):
        """Return a tree's namespaces, mapped to prefixes. the default namespace is replaced with 'tei'"""
        if isinstance(self.xml, etree._ElementTree):
            nsmap = self.xml.getroot().nsmap
        elif isinstance(self.xml, etree._Element):
            nsmap = self.xml.nsmap

        for k, v in nsmap.items():
            if k is None:
                nsmap["tei"] = nsmap.pop(None)
        return nsmap

    def entities(self):
        """Return the attributes of all <rs>-tags in the document.

        Entities such as 'parents' are a nnotated as two entities, key='524 526',
        so they'll be represented as separate persons

        """
        entities = defaultdict(list)

        for e in self.xml.xpath("//tei:rs", namespaces=self.nsmap):
            ents = entities[e.get("type")]
            entities[e.get("type")].extend(
                [k for k in e.get("key", "").split() if k not in ents]
            )
        return entities

    def text(self, layers=False):
        """
        Return the first div in the <body> as a single string. Strips whitespace.

        Parameters
        ----------
        layers: bool
            if true, return a list with the text of each <div> in the <body>
        """
        text = []
        for d in self.xml.xpath("//tei:text//tei:body//tei:div", namespaces=self.nsmap):
            layer = []
            for elt in d:
                if elt.tag == f"{{{self.nsmap['tei']}}}div":
                    continue
                layer.append(elt.xpath("string()").strip())
            text.append(" ".join(layer))

        return text if layers else text[0]

    def _unicode_characters(self):
        """Return all unique unicode codepoints in the original text."""

        def is_unicode(char):
            try:
                char.encode("ascii")
            except UnicodeEncodeError:
                return True
            return False

        chars = []
        for c in {ch for ch in self.text()}:
            if is_unicode(c):
                chars.append(
                    {
                        "character": c,
                        "codepoint": f"0x{ord(c):04x}",
                        "category": unicodedata.category(c),
                        "name": unicodedata.name(c),
                    }
                )
        return chars

    # def normalize_unicode(self, text):

    #     common_symbols = {
    #         r"\s+": " ",
    #         "\u00a0": " ",  # NO-BREAK SPACE
    #         # "\u00a3": "",  # POUND SIGN
    #         # "\u00b0": "",  # DEGREE SIGN
    #         # "\u00b1": "+-",  # PLUS-MINUS SIGN
    #         # "\u00b4": "",  # ACUTE ACCENT
    #         "\u00b7": ".",  # MIDDLE DOT
    #         # "\u00bd": "1/2",  # VULGAR FRACTION ONE HALF
    #         "\u2013": "-",  # EN DASH
    #         "\u2014": "-",  # EM DASH
    #         "\u201c": '"',  # LEFT DOUBLE QUOTATION MARK
    #         "\u201d": '"',  # RIGHT DOUBLE QUOTATION MARK
    #         "\u2018": "'",  # LEFT SINGLE QUOTATION MARK
    #         "\u2019": "'",  # RIGHT SINGLE QUOTATION MARK
    #         "\u00bb": '"',  # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    #         "\u00bb": '"',  # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    #         "\u2026": "",  # HORIZONTAL ELLIPSIS
    #         "\u2500": "",  # BOX DRAWINGS LIGHT HORIZONTAL
    #         "\u25a1": "",  # WHITE SQUARE
    #         "- ": "",
    #     }
    #     for k, v in common_symbols.items():
    #         text = re.sub(k, v, text)

    #     return text

    def language(self):
        return langdetect.detect(self.text())
