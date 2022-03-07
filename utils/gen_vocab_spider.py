import json
import spacy
import sys

from utils.gen_vocab import COUNT

nlp = spacy.load("en_core_web_sm")
print("loaded")

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
COUNT = sys.argv[3]
SQL_FUNC_VOCAB = ['avg','count','first','last','sum','min','max','date','year','for','by']

sql_vocab = {}
table_props={}
pairs=[]
index=0

with open('/content/Sent2LogicalForm/data/sql_vocab.txt') as vocab_file:
    tokens = vocab_file.readlines()
    for token in tokens:
        sql_vocab[token.lower()] = True

with open('/content/Sent2LogicalForm/data/tables.json') as file:
    table_data = json.load(file)
    for entry in table_data:
        table_props[entry['db_id']]['columns'] = [column[1].lower() for column in entry['column_names_original']]
        if 'table_names' in table_props:
            for table_name in entry['table_names_original']:
                table_props['table_names'][table_name] = True
        else: table_props['table_names'] = {}

sql_tokens = {
    'column' : '<attr>',
    'alais' : '<al>',
    'table' : '<table>'
}

# Opening JSON file
with open(INPUT_FILE) as json_file:
    data = json.load(json_file)
    for entry in data:
        print(index)
        tokens = list(entry['question_toks'])
        for i in range(0,len(tokens)):
            pos_tag = nlp(tokens[i])[0]
            if pos_tag.lemma_ in table_props[entry['db_id']]['columns']:
                tokens[i] = sql_tokens['column']
            if pos_tag.lemma_ in table_props[entry['db_id']]['table_names']:
                tokens[i] = sql_tokens['table']
        sql_tokens = list(entry['query_toks'])
        for i in range(0,len(sql_tokens)):
            if sql_tokens[i] in sql_vocab or sql_tokens[i] in SQL_FUNC_VOCAB:
                continue
            if '.' in list(sql_tokens[i]) and len(sql_tokens[i].split('.'))==2:
                sql_tokens[i] = sql_tokens['alais']+'.'+sql_tokens['column']
            if sql_tokens[i] in table_props[entry['db_id']]['columns']:
                sql_tokens[i] = sql_tokens['column']
            if sql_tokens[i] in table_props[entry['db_id']]['table_names']:
                sql_tokens[i] = sql_tokens['table']
        sentence = ' '.join(tokens)
        sql = ' '.join(sql_tokens)
        print(sentence)
        print(sql)
        print("")
        pairs.append((sentence,sql))
        index+=1
        if index==COUNT:
            break

with open(OUTPUT_FILE,'w',encoding='utf-8') as train_file :
    for pair in pairs:
        print(pair)
        train_file.write(pair[0] + "   " + pair[1] + "\n")