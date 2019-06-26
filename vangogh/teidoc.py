from collections import defaultdict
from lxml import etree
import re
import unicodedata

import langdetect

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
        self.tree = etree.tostring(self.xml)
        self.nsmap = self._get_nsmap()

    def _get_nsmap(self):
        nsmap = self.xml.getroot().nsmap
        for k, v in nsmap.items():
            if k is None:
                nsmap["tei"] = nsmap.pop(None)
        return nsmap

    def _element_map(self, element):
        return etree.QName(element.tag).localname, dict(map(self._element_map, element)) or element.text

    def metadata(self):
        """ teiHeader """
        tree = etree.fromstring(self.tree)
        return self._element_map(tree.xpath("//tei:teiHeader", namespaces=self.nsmap)[0])

        # lh = tree.xpath(
        #     "//tei:teiHeader//tei:sourceDesc/vg:letDesc/vg:letHeading",
        #     namespaces=self.nsmap,
        # )[0]
        # metadata = {
        #     "name": "let" + let_id if "RM" not in let_id else let_id,
        #     "author": lh[0].text,
        #     "addressee": lh[1].text,
        #     "place": lh[2].text,
        #     "date": lh[3].text,
        # }

    def entities(self):
        """ alle rs-elementene: <rs type=aaa key=000></rs> """

        pass
        # entities = []
        # for e in tree.xpath("//tei:rs", namespaces=self.nsmap):
        #     try:
        #         content = e.xpath(".//text()")[0]
        #     except:
        #         print(f"leeg element -- {let_id}: {etree.tostring(e)}")
        #         entities.append(
        #             (e.get("type"), e.get("key").split(), re.sub(r"\s+", r" ", content))
        #             )
        #     except TypeError:
        #         print(f"{let_id}: {etree.tostring(e)}")
        #         raise
        # return entities

    def text(self):
        tree = etree.fromstring(self.xml)
        text = []
        for d in tree.xpath("//tei:text//tei:body//tei:div", namespaces=self.nsmap):
            layer = []
            for elt in d:
                if elt.tag == f"{{{self.nsmap['tei']}}}div":
                    continue
                layer.append("".join(elt.xpath(".//text()")))
            text.append("".join(layer))
        return text

    def unicode_characters(self):
        pass

    def processing_pipe(self, funcs):
        self.pipeline.append(*funcs)

    def processed_text(self):
        proc_text = self.text()
        for fun in self.pipeline:
            proc_text = fun(proc_text)
        return proc_text

    def lang(self):
        return langdetect.detect(self.text())
