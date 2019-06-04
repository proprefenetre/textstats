from lxml import etree

parser = etree.XMLParser(attribute_defaults=True)
tree = etree.parse("/home/niels/projects/vangogh/letters/let001a.xml", parser)

root = tree.getroot()

for e in root[2][0][1]:
    for l in e:
        print(l.tag)
