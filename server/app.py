from flask import request
from flask import Flask
from model import getSavedModels
from sql_utils import ColumnsRanker
from sql_utils import predict_table_from_model
from sql_utils import extract_value
from sql_utils import get_tables_info, post_process_query,getLangs,predict_query
from db import Database
from flask_cors import CORS

device="cpu"
SOS_token = 0
EOS_token = 1
ENCODER_PATH = r'C:\Users\admin\Desktop\Sent2LogicalForm\models\spider\encoder.pth'
DECODER_PATH = r'C:\Users\admin\Desktop\Sent2LogicalForm\models\spider\decoder.pth'
TABLE_PREDICTOR_PATH = r'C:\Users\admin\Desktop\Sent2LogicalForm\models\spider\table_pred.pth'
LANG_FILE_PATH = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\train_spider.txt'
TABLE_PROPS_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\table_props.json'
SQL_VOCAB_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\sql_vocab.txt'
DB_FILES = r"C:\Users\admin\Desktop\Sent2LogicalForm\database"

app = Flask(__name__)
CORS(app=app)
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

print("Getting table info...")
table_props = get_tables_info(TABLE_PROPS_FILE)
tables = Database().get_tables()

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
        input_lang_sql,
        sql_output_lang,
        device
    )
    print(output)
    table = predict_table_from_model(table_predictor,sentence,input_lang_table,table_output_lang)
    print(table)
    refined_query = post_process_query(
        output,
        table,
        table_props
    )
    print(refined_query)
    columns = Database().get_columns(table)
    print(columns)
    final_query = ColumnsRanker(input_lang_sql,sql_output_lang).get_final_query(sentence,refined_query,columns,len(columns))
    print(final_query)
    
    return {
        "output" : final_query,
        "table" : table
    }

@app.route("/tranx", methods=['GET', 'POST'])
def get_tranx_output():
    return {
        "output" : "Model under construction"
    }

@app.route("/execute",methods=['POST'])
def execute_query():
    query = request.json['query']
    table =  request.json['table']
    print(table_props['table_names'][table])
    if table_props['table_names'][table] not in tables :
        return {
           "result" : "Table not present in db"
        }
    return {
        "result" : Database().execute(query)
    }