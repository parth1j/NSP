import spacy
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('merge_noun_chunks')
query = "What are the names of the heads who are born outside the California state?"
print([(c.text,c.pos_) for c in nlp(query)])


