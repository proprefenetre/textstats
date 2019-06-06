from pprint import pprint
import spacy

from letter import Letter

corpus = [Letter(f"/home/niels/projects/vangogh/letters/let0{n:0>2}.xml") for n in range(1, 11)]

nlp = spacy.load('nl_core_news_sm')

l = nlp(corpus[0].original_text())
l_strip = nlp(corpus[0].original_text(strip=True))
l_lower = nlp(corpus[0].original_text(strip=True, lower=True))

ents = [(e.text, e.start_char, e.end_char, e.label_) for e in l.ents]
s_ents = [(e.text, e.start_char, e.end_char, e.label_) for e in l_strip.ents]

pprint(ents)
pprint(s_ents)
