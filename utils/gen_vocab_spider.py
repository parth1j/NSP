import json
import spacy
import sys

nlp = spacy.load("en_core_web_sm")
print("loaded")

INPUT_FILES = [
    '/content/Sent2LogicalForm/data/train_spider.json',
    '/content/Sent2LogicalForm/data/train_others.json',
    '/content/Sent2LogicalForm/data/dev.json'
]
OUTPUT_FILE = sys.argv[1]
COUNT = int(sys.argv[2])
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
        table_props[entry['db_id']] = {}
        table_props[entry['db_id']]['columns'] = [column[1].lower() for column in entry['column_names_original']]
        if 'table_names' in table_props:
            for table_name in entry['table_names_original']:
                table_props['table_names'][table_name] = True
        else: table_props['table_names'] = {}

sql_literals = {
    'column' : '<attr>',
    'alais' : '<al>',
    'table' : '<table>'
}


# Opening JSON file
for INPUT_FILE in INPUT_FILES:
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for entry in data:
            print(index)
            tokens = ' '.join(list(entry['question_toks'])).lower().split(" ")
            for i in range(1,len(tokens)):
                pos_tag = nlp(tokens[i])[0]
                if pos_tag.pos_ not in ['PUNCT']:
                    tokens[i] = pos_tag.lemma_
            sql_tokens = list(entry['query_toks_no_value'])
            alias_table={}
            if "join" in sql_tokens:
                continue
            for i in range(0,len(sql_tokens)):
                if sql_tokens[i] in sql_vocab or sql_tokens[i] in SQL_FUNC_VOCAB:
                    continue
                elif sql_tokens[i]=='``':
                    sql_tokens[i]=""
                elif sql_tokens[i] in table_props[entry['db_id']]['columns']:
                    sql_tokens[i] = sql_literals['column']
                elif sql_tokens[i] in table_props['table_names']:
                    sql_tokens[i] = sql_literals['table']
            
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