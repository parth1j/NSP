import unicodedata
import json
import spacy
import torch
import re
import torch.nn.functional as F

tok = spacy.load('en_core_web_sm')
SQL_FUNC_VOCAB = ['avg','count','first','last','sum','min','max','date','year','for','by']
SOS_token = 0
EOS_token = 1

def tokenize (text):
    regex = re.compile('[' + re.escape('"#$%()&\'+,-./:;@[\]^_`{|}~') + 'r\\t\\n]') # remove punctuation and numbers
    nopunct = regex.sub("", text.lower())
    nopunct = re.sub(' +', ' ', nopunct)
    return [token.text for token in tok.tokenizer(nopunct)]

def agg_token(
    query,
    query_index
):
    agg = query[query_index]
    if query[query_index+1] =='<col>':
        query[query_index+1]=''
        return query,agg + '( ' + '<col>' +' ),' 
    elif query[query_index+1]=='distinct':
        query[query_index+1]=''
        query[query_index+2]=''
        return query,f'{agg}(distinct <col> ),'
    return query, agg + '(*)'


def post_process_query(
    query,
    table,
    table_props
):
    refined_query = ""
    query = re.sub('<table>+','<table>',query)
    query_tokens = query.split(" ")
    for index in range(0,len(query_tokens)):
        token = query_tokens[index]
        if token in SQL_FUNC_VOCAB: #agg function
            tokens,token = agg_token(query_tokens,index)
            refined_query += token + " "
            query_tokens = tokens
        elif token=="<table>":
            refined_query += table + " "
        elif token in table_props['table_names'] :
            refined_query += table_props['table_names'][token] + " "
        elif token=='<EOS>':
            continue
        else: refined_query+=query_tokens[index] + " "
    return refined_query

class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS",2:"<UNK>"}
        self.n_words = 3  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    return s

def getLangs(lang_file):
    lang_file_2 = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\train_tables.txt'
    input_lang_sql = Lang('english')
    input_lang_table = Lang('english')
    output_lang = Lang('sql')
    table_lang = Lang('table')
    lines = open(lang_file, encoding='utf-8').read().strip().split('\n')
    pairs1 = [[normalizeString(s) for s in l.split('   ')] for l in lines]
    lines = open(lang_file_2, encoding='utf-8').read().strip().split('\n')
    pairs2 = [[normalizeString(s) for s in l.split('   ')] for l in lines]
    for pair in pairs1:
        input_lang_sql.addSentence(pair[0])
        output_lang.addSentence(pair[1])
    for pair in pairs2:
        input_lang_table.addSentence(pair[0])
        table_lang.addWord(pair[1])
    return input_lang_sql,input_lang_table, output_lang,table_lang
    
def indexesFromSentence(lang, sentence):
    result=[]
    for word in sentence.split(' '):
      if word not in lang.word2index:
        result.append(1)
      else : result.append(lang.word2index[word])
    return result

def tensorFromSentence(lang, sentence):
    indexes = indexesFromSentence(lang, sentence)
    indexes.append(EOS_token)
    return torch.tensor(indexes, dtype=torch.long, device="cpu").view(-1, 1)

def tensorFromWord(lang,word):
  if word not in lang.word2index:
    index = lang.word2index["UNK"]
  else:
    index = lang.word2index[word]
  return torch.tensor(F.one_hot(torch.tensor([index]), num_classes=lang.n_words),dtype=torch.float32)

def get_tables_info(table_file_path):
    with open(table_file_path) as file:
        table_props = json.load(file)
        table_props['table_names']['<unk>'] = None
    return table_props

def predict_query(
    encoder,
    decoder,
    sentence,
    input_lang,
    output_lang,
    device,
    max_length=5000
):
    sentence = ' '.join(tokenize(sentence))
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

from db import columns
def predict_table_from_model(
    encoder,
    sentence,
    input_lang,
    output_lang
):
    sentence = sentence.split(' ')
    print(sentence)
    for table in list(columns.keys()):
        if table.lower() in sentence:
            return table
    return '<table>'

def preprocess(sentence):
    return ' '.join(tokenize(sentence))