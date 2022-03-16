import os
from flask import request
from flask import Flask
from model import getSavedModels
from sql_utils import get_tables_info, post_process_query,getLangs,predict_query
from db import Database
from flask_cors import CORS

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

app = Flask(__name__)
CORS(app=app)
print("Generating vocab...")
input_lang, sql_output_lang,table_output_lang = getLangs(LANG_FILE_PATH)

print("Generating models...")
encoder,decoder,table_predictor = getSavedModels(
    ENCODER_PATH,
    DECODER_PATH,
    TABLE_PREDICTOR_PATH,
    input_lang,
    sql_output_lang,
    device
)

print("Getting table info...")
table_props = get_tables_info(TABLE_PROPS_FILE)
dir_list = list(table_props.keys())
dir_list.remove("table_names")
db_files_dict = {}
for dir in dir_list:
    file_list = os.listdir(DB_FILES + "/" + dir)
    for file in file_list:
        if(file.endswith('.sqlite')):
            db_files_dict[dir] = file 

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/yale", methods=['GET', 'POST'])
def get_yale_output():
    sentence = request.json['sentence']
    output = predict_query(
        encoder,
        decoder,
        sentence,
        input_lang,
        sql_output_lang,
        device
    )
    refined_query,db_id = post_process_query(
        output,
        table_predictor,
        input_lang,
        table_output_lang,
        table_props
    )
    return {
        "output" : refined_query,
        "db_id" : db_id
    }

@app.route("/tranx", methods=['GET', 'POST'])
def get_tranx_output():
    return {
        "output" : "Model under construction"
    }

@app.route("/execute",methods=['POST'])
def execute_query():
    query = request.json['query']
    db_id =  request.json['db_id']
    db_file = db_files_dict[db_id]
    db = Database(db_file)
    return {
        "result" : db.execute(query)
    }
