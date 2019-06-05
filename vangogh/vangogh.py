from lxml import etree
import re

# tree = etree.parse("/home/niels/projects/vangogh/letters/let001a.xml", parser)

class Letter:

    def __init__(self, xml, parser=etree.XMLParser(attribute_defaults=True), namespaces={"tei": "{http://www.tei-c.org/ns/1.0}"}):
        self.xml = etree.parse(xml, parser)
        self.namespaces = namespaces

    def people(self):
        names = {}
        find = etree.ETXPath("//{http://www.tei-c.org/ns/1.0}rs")
        for e in find(self.xml):
            names[re.sub(r'\s+', r' ', e.text)] = e.get('key')
        return names

    def original_text(self):
        find = etree.ETXPath("//{http://www.tei-c.org/ns/1.0}div[@type=\"original\"]//text()")
        text = ''.join(find(self.xml))
        text = re.sub(r'\s+', r' ', text)
        text = re.sub(r'[–&.,!?;()]+', r'', text)
        return text.lower()



l = Letter("/home/niels/projects/vangogh/letters/let001a.xml")
print(l.original_text())
