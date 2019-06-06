import spacy

corpus = [Letter(f"/home/niels/projects/vangogh/letters/let0{n:0>2}.xml").original_text() for  n in range(1, 11)]

nlp = spacy.load('nl_core_news_sm')
l = nlp(corpus[0])
for t in l:
    print(t.text, t.pos_, t.dep_)
