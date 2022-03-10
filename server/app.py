from flask import request
from flask import Flask
import torch
from model import getSavedModel
from sql_utils import preprocess, getLangs, tensorFromSentence
from db import Database
from flask_cors import CORS
device="cpu"

SOS_token = 0
EOS_token = 1
sql_literals = {
    'column' : '<attr>',
    'alais' : '<al>',
    'table' : '<table>'
}
ENCODER_PATH = r'C:\Users\admin\Desktop\Sent2LogicalForm\models\spider\encoder (2).pth'
DECODER_PATH = r'C:\Users\admin\Desktop\Sent2LogicalForm\models\spider\decoder (2).pth'

app = Flask(__name__)
CORS(app=app)

input_lang, output_lang = getLangs()
encoder,decoder = getSavedModel(ENCODER_PATH,DECODER_PATH,input_lang,output_lang,"cpu")

def evaluate(encoder, decoder, sentence, max_length=5000):
    sentence,columns,tables = preprocess(sentence)
    with torch.no_grad():
        input_tensor = tensorFromSentence(input_lang, sentence)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()
        encoder_output = encoder.initHidden()
        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],encoder_output,encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS
        decoder_hidden = encoder_hidden
        decoder_context = encoder_output
        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(max_length):
            decoder_output, (decoder_hidden,decoder_context), decoder_attention = decoder(decoder_input, decoder_context,decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(output_lang.index2word[topi.item()])

            decoder_input = topi.squeeze().detach()
        return ' '.join(decoded_words)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/yale", methods=['GET', 'POST'])
def get_yale_output():
    sentence = request.json['sentence']
    output = evaluate(encoder,decoder,sentence)
    return {
        "output" : output
    }

@app.route("/tranx", methods=['GET', 'POST'])
def get_tranx_output():
    return {
        "output" : "Model under construction"
    }

@app.route("/execute",methods=['POST'])
def execute_query():
    return None
