from lxml import etree
import re

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
        find_textual_notes = etree.ETXPath("//{http://www.tei-c.org/ns/1.0}div[@type=\"textualNotes\"]")
        for e in find_textual_notes(self.xml):
            e.getparent().remove(e)
        find = etree.ETXPath("//{http://www.tei-c.org/ns/1.0}div[@type=\"original\"]//text()")
        text = ''.join(find(self.xml))
        text = re.sub(r'[\s’]+', r' ', text)
        text = re.sub(r'[–&.,!?;()\\\/─_“”‘-]+', r'', text)
        return text.lower()


for n in range(1, 11):
    l = Letter(f"/home/niels/projects/vangogh/letters/let0{n:0>2}.xml")
    print(l.original_text())
