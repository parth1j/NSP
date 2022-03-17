from sql_utils import predict_table_from_model
from model import getSavedModels
from sql_utils import getLangs
import unicodedata
import json
import spacy
import sys
import re
import string

PROPS_FILE = r"C:\Users\admin\Desktop\Sent2LogicalForm\data\table_props.json"

table_props={}
pairs_sent_sql=[]
pairs_sent_table=[]
index=0

device="cpu"
SOS_token = 0
EOS_token = 1
ENCODER_PATH = r'C:\Users\admin\Desktop\Sent2LogicalForm\models\spider\encoder (1).pth'
DECODER_PATH = r'C:\Users\admin\Desktop\Sent2LogicalForm\models\spider\decoder (1).pth'
TABLE_PREDICTOR_PATH = r'C:\Users\admin\Desktop\Sent2LogicalForm\models\spider\table_pred.pth'
LANG_FILE_PATH = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\train_spider.txt'
TABLE_PROPS_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\table_props.json'
SQL_VOCAB_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\sql_vocab.txt'
DB_FILES = r"C:\Users\admin\Desktop\Sent2LogicalForm\database"

def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    return s

print("Generating vocab...")
input_lang_sql, input_lang_table ,sql_output_lang,table_output_lang = getLangs(LANG_FILE_PATH)

print("Generating models...")
encoder,decoder,table_predictor = getSavedModels(
    ENCODER_PATH,
    DECODER_PATH,
    TABLE_PREDICTOR_PATH,
    input_lang_sql,
    input_lang_table,
    sql_output_lang,
    table_output_lang,
    device
)



tok = spacy.load('en_core_web_sm')
def tokenize (text):
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]') # remove punctuation and numbers
    nopunct = regex.sub("", text.lower())
    nopunct = re.sub(' +', ' ', nopunct)
    return [token.text for token in tok.tokenizer(nopunct)]

with open(r'C:\Users\admin\Desktop\Sent2LogicalForm\data\tables.json') as file:
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


with open(PROPS_FILE,'w',encoding='utf-8') as json_file :
    json_file.truncate(0)
    json.dump(table_props,json_file)