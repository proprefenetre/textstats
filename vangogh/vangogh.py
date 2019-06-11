from codepoints import process
from pprint import pprint
import re
import spacy
from spacy.lang.nl.stop_words import STOP_WORDS

# nlp = spacy.load('nl_core_news_sm')

from letter import Letter

corpus = [Letter(f"/home/niels/projects/vangogh/letters/let{n:0>3}.xml") for n in range(1, 11)]

text = ''.join([l.preprocess() for l in corpus])
