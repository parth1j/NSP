import unicodedata
import json
import spacy
import torch
import re
import string
import torch.nn.functional as F

tok = spacy.load('en_core_web_sm')
SQL_FUNC_VOCAB = ['avg','count','first','last','sum','min','max','date','year','for','by']
SOS_token = 0
EOS_token = 1

def tokenize (text):
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]') 
    nopunct = regex.sub("", text.lower())
    nopunct = re.sub(' +', ' ', nopunct)
    return [token.text for token in tok.tokenizer(nopunct)]

def agg_token(
    query,
    query_index
):
    agg = query[query_index]
    if query[query_index+1] =='<col>':
        return agg + '(' + '<col>' +')' 
    return agg + '(*)'

def column_token(
    query,
    query_index,
    column_dict
):
    if query[query_index+1] in column_dict:
        return column_dict[query[query_index+1]] 
    return "<unk_col>"

def value_token_column(value,pre_token):
    return f'= "{value}" ' if pre_token!='limit' else value 

def extract_value(sentence):
    tokens = preprocess(sentence)
    value_table=[]
    value_table.append(token for token in tokens if tok(token)[0].pos_ in ['PRON','NUM'])

def post_process_query(
    query,
    model,
    input_lang,
    output_lang,
    table_props,
    value_table
):
    refined_query = ""
    query_tokens = query.split(" ")
    table = predict_table_from_model(model,query,input_lang,output_lang)
    db_id = table_props['table_names'][table][0]
    value_index=0
    for index in range(0,len(query_tokens)):
        token = query_tokens[index]
        if token in SQL_FUNC_VOCAB: #agg function
            if db_id is not None:
                refined_query += agg_token(query_tokens,index,table_props[db_id]['columns']) + " "
            else : refined_query += agg_token(query_tokens,index,{}) + " "
        elif token=="value":
            if value_index < len(value_table):
                refined_query += value_token_column(value_table[value_index],query_tokens[index-1]) + " "
                value_index+=1
        elif token=="<table>":
            refined_query += table_props['table_names'][table][1] + " "
        elif token=='<EOS>':
            continue
        else: refined_query+=query_tokens[index] + " "
    return refined_query,db_id,table_props[db_id]['columns']

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
    lang_file_2 = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\train_spider (3).txt'
    input_lang = Lang('english')
    output_lang = Lang('sql')
    table_lang = Lang('table')
    lines = open(lang_file, encoding='utf-8').read().strip().split('\n')
    pairs1 = [[normalizeString(s) for s in l.split('   ')] for l in lines]
    lines = open(lang_file_2, encoding='utf-8').read().strip().split('\n')
    pairs2 = [[normalizeString(s) for s in l.split('   ')] for l in lines]
    for pair in pairs1:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
    for pair in pairs2:
        table_lang.addSentence(pair[2] if len(pair)==3 else pair[1])
    return input_lang, output_lang,table_lang
    
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

def get_sql_vocab(sql_vocab_file_path):
    sql_vocab={}
    with open(sql_vocab_file_path) as vocab_file:
        tokens = vocab_file.readlines()
        for token in tokens:
            sql_vocab[token.lower()] = True
    return sql_vocab

def get_tables_info(table_file_path):
    with open(table_file_path) as file:
        table_props = json.load(file)
        table_props['table_names']['<unk>'] = None
        keys = list(table_props['table_names'].keys())
        table_props['table_names'] = {}
        for key in keys:
            table_props['table_names'][''.join(tokenize(key))] = (table_props['table_names'][key],key)
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
    sentence = ' '.join(preprocess(sentence))
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

def predict_table_from_model(
    encoder,
    sentence,
    input_lang,
    output_lang
):
    sentence = ' '.join(preprocess(sentence))
    with torch.no_grad():
        input_tensor = tensorFromSentence(input_lang, sentence)
        y_pred =  encoder(input_tensor)
        return output_lang.index2word[int(torch.argmax(y_pred))]

def preprocess(sentence):
  return tokenize(sentence)