from collections import defaultdict
from lxml import etree
import re

parser = etree.XMLParser(attribute_defaults=True)
tree = etree.parse("/home/niels/projects/vangogh/letters/let001a.xml", parser)

NS = {"t": "{http://www.tei-c.org/ns/1.0}"}

doc = tree.getroot()

names = defaultdict(set)
for e in doc.iter(tag=f"{NS['t']}rs"):
   names[e.get('key')].add(re.sub(r"\s+", r" ", e.text))

# for e in doc.iter(tag=f"{NS['t']}div"):
#     print(e.text)
