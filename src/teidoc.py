from collections import defaultdict
import html
import io
import logging
from lxml import etree, objectify
import os.path
import unicodedata


log = logging.getLogger(__name__)


class TEIDocument:
    """This class represents a TEI-document

    Parameters
    ----------
    parser:
        An instance of an etree.XMLParser.
    """

    def __init__(self, parser=etree.XMLParser(recover=True)):
        self.parser = parser
        self.tree = None
        self.nsmap = None

    @classmethod
    def from_tree(cls, tree):
        td = cls()
        td.tree = tree
        td.nsmap = td._get_nsmap()

        return td

    @classmethod
    def from_path(cls, path):
        td = cls()
        td.load(path)

        return td

    def load(self, source):
        """ Read source from file and parse it.

        Parameters
        ----------
        source: string containing the path to an source-file or source.
        """
        if not source:
            raise ValueError("No file provided")

        if isinstance(source, io.IOBase):
            xml = source.read()
            log.debug(f"source: {type(source)}")
            log.debug(f"xml: {type(xml)}")
        elif os.path.isfile(os.path.abspath(source)):
            log.debug(f"source: '{source}'")
            with open(source, "r") as f:
                xml = f.read()

        if isinstance(xml, bytes):
            log.debug(f"type xml: {type(xml)} - decoding to str")
            xml = xml.decode()

        xml = html.unescape(xml).encode("utf-8")

        self.tree = etree.fromstring(xml, self.parser)

        self.nsmap = self._get_nsmap()
        log.debug(f"loaded: {type(self.tree)}")

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
        if self.nsmap:
            expr = "//tei:rs"
        else:
            expr = "//rs"

        for e in self.tree.xpath(expr, namespaces=self.nsmap):
            ents = entities[e.get("type")]
            entities[e.get("type")].extend(
                # filter
                [k for k in e.get("key", "").split() if k not in ents]
            )
        return entities

    def text(self, kind=None):
        """
        Extract text from the divs in the text-element

        Parameters:
        -----------
            kind: if None, return a defaultdict(list) of 'type': [text, ...] pairs. If specified, return a list
            containing the text found in divs of that kind

        Raises:
        -------
            KeyError: if kind is specified but not present in the document

        """
        text = defaultdict(list)
        expr = "//tei:text//tei:body//tei:div"
        if not self.nsmap:
            expr = expr.replace("tei:", "")

        log.debug(f"using namespaces: {self.nsmap}")

        for d in self.tree.xpath(expr, namespaces=self.nsmap):
            layer = []
            for elt in d:
                # prevent nested layers
                if self._clean_tag(elt) == "div":
                    log.debug(f"nested div found in {'/'.join(self._ancestors(elt))}")
                    continue
                layer.append(elt.xpath("string()").strip())
            text[d.get("type", "default")].append(" ".join(layer))
            log.debug(f"layers: {text.keys()}")

        if kind:
            if kind in text:
                return text[kind]
            else:
                raise KeyError(f"{kind} not in text")
        return text

    def _ancestors(self, elt):
        return [self._as_xpath(e) for e in reversed(list(elt.iterancestors()))]

    def _descendants(self, elt):
        return [self._as_xpath(e) for e in reversed(list(elt.iterdescendants()))]

    def _as_xpath(self, elt):
        attr = ", ".join(f"@{k}=\"{v}\"" for k, v in elt.items())
        return f"{self._clean_tag(elt)}[{attr}]" if attr else f"{self._clean_tag(elt)}"

    def _clean_tag(self, elt):
        return etree.QName(elt).localname

    def _as_ElementTree(self):
        return etree.ElementTree(self.tree)

    def _get_nsmap(self):
        """ Return a tree's namespaces, mapped to prefixes.

        the default namespace is replaced with 'tei'
        """
        nsmap = None
        if isinstance(self.tree, etree._ElementTree):
            nsmap = self.tree.getroot().nsmap
        elif isinstance(self.tree, etree._Element):
            nsmap = self.tree.nsmap

        if not nsmap:
            log.warning(f"No namespaces in document.")
        else:
            nsmap["tei"] = nsmap.pop(None)
            log.debug(f"Replaced default namespace: {nsmap}")
        return nsmap

    def _clear_namespaces(self):
        root = etree.fromstring(etree.tostring(self.tree))
        for elt in root.getiterator():
            elt.tag = etree.QName(elt).localname
        objectify.deannotate(root, cleanup_namespaces=True)
        return root
