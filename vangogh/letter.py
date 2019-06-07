from lxml import etree
import re
import string

class Letter:

    def __init__(self, xml, parser=etree.XMLParser(attribute_defaults=True), namespaces={"tei": "{http://www.tei-c.org/ns/1.0}"}):
        self.xml = etree.parse(xml, parser)
        self.namespaces = namespaces

    def people(self):
        names = {}
        find_names = etree.ETXPath("//{http://www.tei-c.org/ns/1.0}rs")
        for e in find_names(self.xml):
            names[re.sub(r'\s+', r' ', e.text)] = e.get('key')
        return names

    def original_text(self):
        find_textual_notes = etree.ETXPath("//{http://www.tei-c.org/ns/1.0}div[@type=\"textualNotes\"]")
        for e in find_textual_notes(self.xml):
            e.getparent().remove(e)
        find = etree.ETXPath("//{http://www.tei-c.org/ns/1.0}div[@type=\"original\"]//text()")
        text = ''.join(find(self.xml))
        if strip:
            text = re.sub(r'[\s’]+', r' ', text)
            text = re.sub(rf'[\–\─\-“”‘{string.punctuation}]+', r'', text)
        if lower:
            text = text.lower()
        return text

    def rare_interpunctie(self):
        find_c = etree.ETXPath("//{http://www.tei-c.org/ns/1.0}c")
        for e in find_c(self.xml):
            return (e.get('type'), e.text)
