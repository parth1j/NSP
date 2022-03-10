import unicodedata
import json
import spacy
import torch
import re
import string

tok = spacy.load('en')
def tokenize (text):
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]') 
    nopunct = regex.sub("", text.lower())
    nopunct = re.sub(' +', ' ', nopunct)
    return [token.text for token in tok.tokenizer(nopunct)]

SQL_FUNC_VOCAB = ['avg','count','first','last','sum','min','max','date','year','for','by']
sql_literals = {
    'column' : '<attr>',
    'alais' : '<al>',
    'table' : '<table>'
}

STD_SQL_QUERY_TOKEN = {
    "select",
    "distinct",
    "agg"
    "column"
    "from",
    "table",
    "where",
    "column",
    "op",
    "value",
    "groupBy",
    "having",
    "orderBy",
    "limit",
    "intersect",
    "union",
    "except"
}

SOS_token = 0
EOS_token = 1

class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS",2:"<UNK>"}
        self.n_words = 3  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    return s

def getLangs():
    input_lang = Lang('english')
    output_lang = Lang('sql')
     # Read the file and split into lines
    lines = open(r'C:\Users\admin\Desktop\Sent2LogicalForm\data\train_spider.txt', encoding='utf-8').read().strip().split('\n')
    # Split every line into pairs and normalize
    pairs = [[normalizeString(s) for s in l.split('   ')] for l in lines]
    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
    return input_lang, output_lang
    
def indexesFromSentence(lang, sentence):
    result=[]
    for word in sentence.split(' '):
      if word not in lang.word2index:
        result.append(1)
      else : result.append(lang.word2index[word])
    return result

def tensorFromSentence(lang, sentence):
    indexes = indexesFromSentence(lang, sentence)
    indexes.append(EOS_token)
    return torch.tensor(indexes, dtype=torch.long, device="cpu").view(-1, 1)

def get_sql_vocab():
    sql_vocab={}
    with open(r'C:\Users\admin\Desktop\Sent2LogicalForm\data\sql_vocab.txt') as vocab_file:
        tokens = vocab_file.readlines()
        for token in tokens:
            sql_vocab[token.lower()] = True
    return sql_vocab

def get_tables_info():
    with open(r'C:\Users\admin\Desktop\Sent2LogicalForm\data\tables_props.json') as file:
        table_props = json.load(file)
    return table_props


def preprocess(sentence):
  return tokenize(sentence)