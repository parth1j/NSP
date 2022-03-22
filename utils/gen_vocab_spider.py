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
tok = spacy.load('en_core_web_sm')
def tokenize (text):
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]') # remove punctuation and numbers
    nopunct = regex.sub("", text.lower())
    nopunct = re.sub(' +', ' ', nopunct)
    return [token.text for token in tok.tokenizer(nopunct)]

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
            tokens=tok(' '.join(tokenize(' '.join(list(entry['question_toks'])))))
            tokens_list = []
            for i in range(1,len(tokens)):
                if tokens[i].pos_ == 'NOUN':
                    tokens_list.append('<NOUN>')
                elif tokens[i].pos_ == 'NUM':
                    tokens_list.append('<NUM>')
                elif tokens[i].pos_ == 'PROPN':
                    tokens_list.append('<PROPN>')
                else : tokens_list.append(tokens[i].lemma_)
            sql_tokens = tokenize(' '.join(list(entry['query_toks_no_value'])))
            sql_tokens_list = []
            table=None
            is_column = 0
            for i in range(0,len(sql_tokens)):
                if sql_tokens[i] == 'from':
                    relevant_tables[sql_tokens[i+1]] = True
                    table = sql_tokens[i+1]
                    sql_tokens_list.append(sql_tokens[i])
                elif sql_tokens[i] in relevant_tables:
                    sql_tokens_list.append('<table>')
                elif sql_tokens[i] in table_props[entry['db_id']]['columns']:
                    is_column+=1
                else:
                    if is_column > 1:
                        sql_tokens_list.append('<cols>')
                        is_column=0
                    elif is_column == 1:
                        sql_tokens_list.append('<col>')
                        is_column=0
                    sql_tokens_list.append(sql_tokens[i])
            sentence = ' '.join(tokens)
            sql = ' '.join(sql_tokens_list)
            print(sentence)
            print(sql)
            print(table)
            print("")
            if "join" not in sql_tokens:
                pairs_sent_sql.append((sentence,sql))
            pairs_sent_table.append((sentence,table))
            index+=1
            if index==COUNT:
                break
    if index==COUNT:
        break

temp = table_props['table_names']
for key in list(temp):
    if key not in relevant_tables:
        del table_props['table_names'][key]

print(len(list(table_props['table_names'])))

with open(OUTPUT_FILE,'w',encoding='utf-8') as train_file :
    train_file.truncate(0)
    for pair in pairs_sent_sql:
        text = pair[0] + "   " + pair[1]
        train_file.write( text + "\n")

with open(TABLES_OUTPUT_FILE,'w',encoding='utf-8') as train_file :
    train_file.truncate(0)
    for pair in pairs_sent_table:
        text = pair[0] + "   " + pair[1]
        train_file.write( text + "\n")

with open(PROPS_FILE,'w',encoding='utf-8') as json_file :
    json_file.truncate(0)
    json.dump(table_props,json_file)