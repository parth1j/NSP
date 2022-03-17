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
OUTPUT_FILE = sys.argv[1]
COUNT = int(sys.argv[2])
PROPS_FILE = "/content/Sent2LogicalForm/data/table_props.json"

table_props={}
pairs=[]
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
            tokens=tokenize(' '.join(list(entry['question_toks'])))
            sql_tokens = tokenize(' '.join(list(entry['query_toks_no_value'])))
            sql_tokens_list = []
            if "join" in sql_tokens:
                continue
            table=None
            is_column = 0
            for i in range(0,len(sql_tokens)):
                if sql_tokens[i] == 'from':
                    relevant_tables[sql_tokens[i+1]] = True
                    table = sql_tokens[i+1]
                    sql_tokens_list.append(sql_tokens[i+1])
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
            pairs.append((sentence,sql,table))
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
    for pair in pairs:
        text = pair[0] + "   " + pair[1]
        if len(pair)==3:
          text +=  "   " + pair[2]
        train_file.write( text + "\n")

with open(PROPS_FILE,'w',encoding='utf-8') as json_file :
    json_file.truncate(0)
    json.dump(table_props,json_file)