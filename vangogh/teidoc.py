import langdetect
from lxml import etree
import re
import unicodedata


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


class TeiDoc:
    def __init__(self, xml, parser=etree.XMLParser(), punct=PUNCT_MAP, nsmap=NSMAP):
        self.punct = punct
        self.nsmap = nsmap
        self.xml = etree.tostring(etree.parse(xml, parser))

    def metadata(self):
        tree = etree.fromstring(self.xml)
        let_id = tree.xpath(
            '//tei:teiHeader//tei:sourceDesc/vg:letDesc/vg:letIdentifier//tei:idno[@type="jlb"]',
            namespaces=self.nsmap,
        )[0].text
        lh = tree.xpath(
            "//tei:teiHeader//tei:sourceDesc/vg:letDesc/vg:letHeading",
            namespaces=self.nsmap,
        )[0]
        entities = []
        try:
            for e in tree.xpath("//tei:rs", namespaces=self.nsmap):
                try:
                    content = e.xpath(".//text()")[0]
                except:
                    print(f"leeg element -- {let_id}: {etree.tostring(e)}")
                entities.append(
                    (e.get("type"), e.get("key").split(), re.sub(r"\s+", r" ", content))
                )
        except TypeError:
            print(f"{let_id}: {etree.tostring(e)}")
            raise

        metadata = {
            "name": "let" + let_id if "RM" not in let_id else let_id,
            "author": lh[0].text,
            "addressee": lh[1].text,
            "place": lh[2].text,
            "date": lh[3].text,
            "entities": entities,
        }

        return metadata

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

    def _rm_punct(self, text):
        for k, v in self.punct.items():
            text = re.sub(k, v, text)
        return text

    def _rm_diacritics(self, text):
        " Remove accented or otherwise decorated characters "
        return "".join(
            c
            for c in unicodedata.normalize("NFKD", text)
            if not unicodedata.combining(c)
        )

    def processed_text(self, punct=True, diac=True):
        text = self.text()[0]
        if punct:
            text = self._rm_punct(text)
        if diac:
            text = self._rm_diacritics(text)
        return text.strip()

    def lang(self):
        return langdetect.detect(self.text()[0])
