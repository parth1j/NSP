import json
import spacy
import sys

nlp = spacy.load("en_core_web_sm")
print("loaded")

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
SQL_FUNC_VOCAB = ['avg','count','first','last','sum','min','max','date','year','for','by']
POS_TAGS = ['NOUN','PROPN']

sql_vocab = {}
pairs=[]
index=0

with open('sql_vocab.txt') as vocab_file:
    tokens = vocab_file.readlines()
    for token in tokens:
        sql_vocab[token.lower()] = True

# Opening JSON file
with open(INPUT_FILE) as json_file:
    data = json.load(json_file)
    print(len(data))
    for entry in data:
        token_index=0
        word_dict = {}
        sentence = ""
        sql = ""
        print(index)
        tokens = list(entry['question_toks'])
        for i in range(0,len(tokens)):
            pos_tag = nlp(tokens[i])[0]
            if pos_tag.pos_ in POS_TAGS :
              word_dict[pos_tag.lemma_] = pos_tag.pos_.lower() + str(token_index)
              token_index+=1
              sentence += word_dict[pos_tag.lemma_] + " "
            elif pos_tag.pos_=='NUM' :
              word_dict[tokens[i]] = "value"
              sentence += word_dict[tokens[i]] + " "
            else :
              sentence += pos_tag.lemma_ + " "
        tokens = list(entry['query_toks_no_value'])
        for i in range(0,len(tokens)):
            pos_tag = nlp(tokens[i])[0]
            if pos_tag.lemma_ in word_dict and tokens[i] not in sql_vocab and tokens[i] not in SQL_FUNC_VOCAB:
                sql = sql + word_dict[pos_tag.lemma_] + " "
            else :
                sql = sql + pos_tag.lemma_ + " "
        print(sentence)
        print(sql)
        print("")
        pairs.append((sentence,sql))
        index+=1

with open(OUTPUT_FILE,'w',encoding='utf-8') as train_file :
    train_file.truncate(0)
    for pair in pairs:
        print(pair)
        train_file.write(pair[0] + "   " + pair[1] + "\n")