from collections import Counter
import spacy
from spacy.lang.nl import STOP_WORDS
from teidoc import TeiDoc

nlp = spacy.load('nl_core_news_sm')

corpus = [nlp(TeiDoc(f"/home/niels/projects/vangogh/letters/let{n:03}.xml").preprocess()) for n in range(1, 200)]
