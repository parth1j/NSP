import spacy

nlp = spacy.load("en_core_web_sm")
print("loaded")
doc = nlp("What are the names of the heads who are born outside the California state?")

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)