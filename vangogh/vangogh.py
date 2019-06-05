from lxml import etree
import re

parser = etree.XMLParser(attribute_defaults=True)
tree = etree.parse("/home/niels/projects/vangogh/letters/let001a.xml", parser)

TEI_NS = "{http://www.tei-c.org/ns/1.0}"
doc = tree.getroot()
for e in doc.iter(tag=f"{TEI_NS}rs"):
   print(re.sub(r"\s+", r" ", e.text))
