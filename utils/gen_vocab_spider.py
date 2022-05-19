import json
import spacy
import sys
import re
import string

INPUT_FILES = [
    '/content/Sent2LogicalForm/data/train_spider.json',
    '/content/Sent2LogicalForm/data/train_others.json',
    '/content/Sent2LogicalForm/data/dev.json'
]
OUTPUT_FILE = '/content/Sent2LogicalForm/data/train_spider.txt'
TABLES_OUTPUT_FILE = '/content/Sent2LogicalForm/data/train_tables.txt'
COUNT = int(sys.argv[1])
PROPS_FILE = "/content/Sent2LogicalForm/data/table_props.json"

table_props={}
pairs_sent_sql=[]
pairs_sent_table=[]
index=0

#tokenization
nlp = spacy.load('en_core_web_sm')


def tokenize (text):
    regex = re.compile('[' + re.escape('"#$%&()\'+,-./:;@[\]^_`{|}~') + '\\r\\t\\n]') # remove punctuation and numbers
    nopunct = regex.sub("", text.lower())
    nopunct = re.sub(' +', ' ', nopunct)
    return [token.text for token in nlp.tokenizer(nopunct)]

with open('/content/Sent2LogicalForm/data/tables.json') as file:
    table_data = json.load(file)
    for entry in table_data:
        table_props[entry['db_id']] = {}
        table_props[entry['db_id']]['columns'] = {} 
        for column in entry['column_names_original']:
            table_props[entry['db_id']]['columns'][''.join(tokenize(column[1]))] = column[1]
        if 'table_names' in table_props:
            for table_name in entry['table_names_original']:
                table_props['table_names'][table_name] = entry['db_id']
        else: table_props['table_names'] = {}

relevant_tables = {}
# Opening JSON file
for INPUT_FILE in INPUT_FILES:
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for entry in data:
            print(index)
            tokens_list = tokenize(' '.join(list(entry['question_toks'])))
            sql_tokens = tokenize(' '.join(list(entry['query_toks'])))
            count  = sql_tokens.count('select')
            if "join"  in sql_tokens or count > 1:
                continue
            sql_tokens_list = [sql_tokens[0]]
            table=None
            is_table = 0
            for i in range(1,len(sql_tokens)):
                if sql_tokens[i] =='from':
                    sql_tokens_list.append(sql_tokens[i])
                    is_table=1
                elif is_table==1:
                  sql_tokens_list.append('<table>')
                  is_table=0
                elif sql_tokens[i] in table_props[entry['db_id']]['columns']:
                  sql_tokens_list.append('<col>')
                else:
                  sql_tokens_list.append(sql_tokens[i])
            sentence = ' '.join(tokens_list)
            sql = ' '.join(sql_tokens_list)
            pairs_sent_sql.append((sentence,sql))
            print(sentence)
            print(sql)
            print("")
            index+=1
            if index==COUNT:
                break
    if index==COUNT:
        break

with open(OUTPUT_FILE,'w',encoding='utf-8') as train_file :
    train_file.truncate(0)
    for pair in pairs_sent_sql:
        text = pair[0] + "   " + pair[1]
        train_file.write( text + "\n")

with open(PROPS_FILE,'w',encoding='utf-8') as json_file :
    json_file.truncate(0)
    json.dump(table_props,json_file)