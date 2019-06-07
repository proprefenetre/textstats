from pprint import pprint

import spacy
from spacy.lang.nl.stop_words import STOP_WORDS

from letter import Letter

corpus = [Letter(f"/home/niels/projects/vangogh/letters/let0{n:0>2}.xml") for n in range(1, 11)]

nlp = spacy.load('nl_core_news_sm')

text = nlp(''.join([l.original_text(process=True) for l in corpus]))
