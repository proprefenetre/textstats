from lxml import etree
import re

# tree = etree.parse("/home/niels/projects/vangogh/letters/let001a.xml", parser)

class Letter:

    def __init__(self, xml, parser=etree.XMLParser(attribute_defaults=True), namespace={"t": "{http://www.tei-c.org/ns/1.0}"}):
        self.parser = parser
        self.xml = etree.parse(xml, parser)
        self.namespace = namespace

    def people(self):
        names = {}
        for e in doc.iter(tag=f"{self.namespace['t']}rs"):
            names[re.sub(r'\s+', r' ', e.text)] = e.get('key')
        return names
