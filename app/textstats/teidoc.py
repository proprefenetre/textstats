from collections import defaultdict
import html
from lxml import etree
import os.path
import unicodedata


class TeiDocument:
    """This class represents a TEI-document

    Parameters
    ----------
    parser:
        An instance of an etree.XMLParser.
    """

    def __init__(self, xml, parser=etree.XMLParser(recover=True)):
        self.parser = parser
        self.tree = self.parse(xml)
        self.nsmap = self._get_nsmap()

    def parse(self, xml):
        if isinstance(xml, (str, bytes)):
            if os.path.isfile(xml):
                with open(xml, "r") as f:
                    xml = f.read()

        if isinstance(xml, bytes):
            xml = xml.decode()

        xml = html.unescape(xml)

        return etree.fromstring(xml.encode("utf-8"), self.parser)

    def _get_nsmap(self):
        """Return a tree's namespaces, mapped to prefixes.

        the default namespace is replaced with 'tei'
        """
        if isinstance(self.tree, etree._ElementTree):
            nsmap = self.tree.getroot().nsmap
        elif isinstance(self.tree, etree._Element):
            nsmap = self.tree.nsmap

        for k, v in nsmap.items():
            if k is None:
                nsmap["tei"] = nsmap.pop(None)
        return nsmap

    def _as_ElementTree(self):
        return etree.ElementTree(self.tree)

    def docinfo(self, attr=None):
        di = self._as_ElementTree().docinfo
        info = {
            "doctype": di.doctype,
            "encoding": di.encoding,
            "externalDTD": di.externalDTD,
            "internalDTD": di.internalDTD,
            "public_id": di.public_id,
            "root_name": di.root_name,
            "standalone": di.standalone,
            "system_url": di.system_url,
            "xml_version": di.xml_version,
        }
        if attr:
            return info.get(attr, None)
        else:
            return info

    def entities(self):
        """Return the attributes of all <rs>-tags in the document.

        Entities such as 'parents' are a nnotated as two entities, key='524 526',
        so they'll be represented as separate persons

        TODO: include names

        """
        entities = defaultdict(list)

        for e in self.tree.xpath("//tei:rs", namespaces=self.nsmap):
            ents = entities[e.get("type")]
            entities[e.get("type")].extend(
                [k for k in e.get("key", "").split() if k not in ents]
            )
        return entities

    def text(self, layers=False):
        """
        Return the first div in the <body> as a single string, unmodified.

        Parameters
        ----------
        layers: bool
            if true, return a list with the text of each <div> in the <body>
        """
        text = []
        for d in self.tree.xpath(
            "//tei:text//tei:body//tei:div", namespaces=self.nsmap
        ):
            layer = []
            for elt in d:
                if elt.tag == f"{{{self.nsmap['tei']}}}div":
                    continue
                layer.append(elt.xpath("string()").strip())
            text.append(" ".join(layer))

        return text if layers else text[0]

    def _unicode_characters(self):
        """Return all unique unicode codepoints in the original text. """

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
