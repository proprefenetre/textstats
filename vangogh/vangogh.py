from codepoints import process
from lxml import etree
from pprint import pprint
import re
# import spacy
# from spacy.lang.nl.stop_words import STOP_WORDS
from teidoc import TeiDoc

# nlp = spacy.load('nl_core_news_sm')
let = TeiDoc("/home/niels/projects/vangogh/letters/let001.xml")

print(let.text())
