from random import sample
import numpy as np
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('bert-base-nli-mean-tokens')
from sql_utils import tokenize
import re

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

class Ranker:
    def __init__(self,values,token) -> None:
        self.max_sim  = -1
        self.max_sim_query = ""
        self.values = values
        self.token = token
        self.permutations = []
    
    def preprocess(self,query):
        regex = re.compile('[' + re.escape('"#$%()&\'+,-./:;@[\]^_`{|}~') + '\\r\\t\\n]') # remove punctuation and numbers
        nopunct = regex.sub("", query.lower())
        nopunct = re.sub('!=','is not equal to',nopunct)
        nopunct = re.sub('=','is equal to',nopunct)
        return nopunct


    def get_final_query(self,sentence,query,no_columns):
        self.max_sim_query = query
        sentence = ' '.join(tokenize(sentence))
        col_token_count = query.count('<col>')
        self.generate_permutations(query,no_columns,col_token_count)
        _set = set()
        for query in self.permutations:
            _set.add(query)
        self.permutations = list(_set)
        self.rank_columns(sentence)
        return self.max_sim_query
    
    def rank_columns(self,sentence):
        for query in self.permutations:
            print(query)
            sentence_embeddings = model.encode([sentence])
            query_embeddings = model.encode([self.preprocess(query)])
            sim = cosine(query_embeddings[0],sentence_embeddings[0])
            print(sim)
            if sim > self.max_sim:
                self.max_sim = sim
                self.max_sim_query = query
        
    def generate_permutations(self,query,no_columns,no_col_tokens):
        if(no_columns==0 or no_col_tokens==0):
            print('query',query)
            self.permutations.append(query)
            return
        for key in self.values:
            temp = re.sub(self.token,str(key),str(query),count=1)
            print('No',no_columns)
            print('temp',temp)
            if temp!=None:
                self.generate_permutations(temp,no_columns-1,no_col_tokens-1)
'''
sample_query = 'SELECT name FROM head WHERE born_state != California'
question =  "What are the names of the heads who are born outside the California state "
columns = ['head_ID', 'name', 'born_state', 'age']
query = 'select <col> from head where <col> != value'

query = Ranker(columns,'<col>').get_final_query(question,query,len(columns))
print(query)
'''

import spacy
nlp = spacy.load('en_core_web_sm')

def get_values(question):
    tokens = nlp(question)
    values = []
    for token in tokens:
        if token.pos_ in ['NUM','PROPN']:
            values.append(token.lemma_)
    return values
'''
query = Ranker(get_values(question),'value').get_final_query(question,query,len(values))
print(query)
'''