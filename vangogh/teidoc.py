from collections import defaultdict
import copy
from lxml import etree, objectify
import re
import unicodedata

import langdetect
import xmltodict

from .utils import flatten_dict

PUNCT_MAP = {
    "\u00a0": " ",  # NO-BREAK SPACE
    "\u00a3": "",  # POUND SIGN
    "\u00b0": "",  # DEGREE SIGN
    "\u00b1": "",  # PLUS-MINUS SIGN
    "\u00b4": "",  # ACUTE ACCENT
    "\u00b7": "",  # MIDDLE DOT
    "\u00bb": "",  # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    "\u00bd": "",  # VULGAR FRACTION ONE HALF
    "\u2013": "",  # EN DASH
    "\u2014": "",  # EM DASH
    "\u2018": "",  # LEFT SINGLE QUOTATION MARK
    "\u201c": "",  # LEFT DOUBLE QUOTATION MARK
    "\u201d": "",  # RIGHT DOUBLE QUOTATION MARK
    "\u2026": "",  # HORIZONTAL ELLIPSIS
    "\u2500": "",  # BOX DRAWINGS LIGHT HORIZONTAL
    "\u25a1": "",  # WHITE SQUARE
    "\u2019": "'",  # RIGHT SINGLE QUOTATION MARK
    "&": "en",
    r"\s+": " ",
    "-": "",
    "_": "",
    "t'": "t",
    "d'": "de ",
    "'t": "het",
    "/": ",",
}


NSMAP = {
    "tei": "http://www.tei-c.org/ns/1.0",
    "vg": "http://www.vangoghletters.org/ns/",
}


class TeiDocument:
    def __init__(self, xml, parser=etree.XMLParser(), punct=PUNCT_MAP, nsmap=NSMAP):
        self.punct = punct
        self.xml = etree.parse(xml, parser)
        self.nsmap = self._get_nsmap()

    def _get_nsmap(self):
        nsmap = self.xml.getroot().nsmap
        for k, v in nsmap.items():
            if k is None:
                nsmap["tei"] = nsmap.pop(None)
        return nsmap

    def metadata(self):
        """ teiHeader """
        teiHeader = self.xml.xpath("//tei:teiHeader//tei:fileDesc", namespaces=self.nsmap)[0]
        return flatten_dict(xmltodict.parse(etree.tostring(teiHeader), xml_attribs=False))

    def entities(self):
        """ Alle rs-elementen: <rs type=aaa key=000></rs>, ignores markup. Entities such as 'parents' are
        a nnotated as two entities, key='524 526', so they'll be represented as separate persons

        """
        entities = defaultdict(set)
        for e in self.xml.xpath("//tei:rs", namespaces=self.nsmap):
            entities[e.get("type")].update(e.get("key", "").split())
        return entities

    def text(self):
        """ Returns the first div in the <body>. Superfluous whitespace is removed. """
        text = []
        for d in self.xml.xpath("//tei:text//tei:body//tei:div", namespaces=self.nsmap):
            layer = []
            for elt in d:
                if elt.tag == f"{{{self.nsmap['tei']}}}div":
                    continue
                layer.append(elt.xpath("string()").strip())
            text.append(re.sub(r"\s+", " ", " ".join(layer)).strip())
        return text[0]

    def unicode_characters(self):
        """ Returns all unique unicode codepoints in the original text """

        def is_unicode(char):
            try:
                char.encode('ascii')
            except UnicodeEncodeError:
                return True
            return False

        return [ch for ch in {c for c in self.text()} if is_unicode(ch)]

    def processing_pipe(self, funcs):
        self.pipeline.append(*funcs)



    def processed_text(self):
        proc_text = self.text()
        for fun in self.pipeline:
            proc_text = fun(proc_text)
        return proc_text

    def lang(self):
        return langdetect.detect(self.text())
