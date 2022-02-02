import csv
import os
from nlp_utils import NLPUtils

FILES = [
    r'C:\Users\admin\Desktop\Sent2LogicalForm\data\train.csv',
    r'C:\Users\admin\Desktop\Sent2LogicalForm\data\test.csv',
    r'C:\Users\admin\Desktop\Sent2LogicalForm\data\validation.csv'
]

NAMES = ['train','test','validation']

INPUT_VOCAB_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\input_vocab.txt'
OUTPUT_VOCAB_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\output_vocab.txt'
TRAIN_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\train.txt'
TEST_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\test.txt'
VALIDATION_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\validation.txt'

input_vocab = {}
output_vocab = {}
train_data=[]
test_data=[]
validation_data=[]
index=0

for i in range(0,len(FILES)):
    with open(FILES[i], encoding="utf8") as csv_file :
        reader = csv.reader(csv_file)
        next(reader)  # skip header
        for row in reader:
            sentence = row[0]
            sent_tokens = NLPUtils.preprocess_sentence(sentence)
            for token in sent_tokens:
                if token in input_vocab:
                    input_vocab[token]+=1
                else:
                    input_vocab[token]=1
            sql = row[1]
            sql_tokens = NLPUtils.preprocess_sentence(sql)
            for token in sql_tokens:
                if token in output_vocab:
                    output_vocab[token]+=1
                else:
                    output_vocab[token]=1
            if NAMES[i]=='train' :
                train_data.append((NLPUtils.to_lower(sentence,True),NLPUtils.to_lower(sql,True)))
            elif NAMES[i]=='test' :
                test_data.append((NLPUtils.to_lower(sentence,True),NLPUtils.to_lower(sql,True)))
            else :
                validation_data.append((NLPUtils.to_lower(sentence,True),NLPUtils.to_lower(sql,True)))
            print(index)
            index+=1

input_vocab = dict(sorted(input_vocab.items(), key=lambda item: item[1]))
output_vocab = dict(sorted(output_vocab.items(), key=lambda item: item[1]))

speech_tags = {}

from nltk import pos_tag
INPUT_FREQ_THRESHOLD = 1000
OUTPUT_FREQ_THRESHOLD = 1000

for key,value in list(input_vocab.items()):
    if input_vocab[key] < INPUT_FREQ_THRESHOLD:
        del input_vocab[key]
        tag = pos_tag([key])
        if tag[0][1]=='NN' or tag[0][1]=='FW':
            if '<NN>' in input_vocab:
                input_vocab['<NN>']+=1
            else:
                input_vocab['<NN>']=1
            speech_tags[key] = '<NN>'
        elif (tag[0][1] =='CD') :
            if '<CD>' in input_vocab:
                input_vocab['<CD>']+=1
            else:
                input_vocab['<CD>']=1
            speech_tags[key] = '<CD>'

for key,value in list(output_vocab.items()):
    if output_vocab[key] < OUTPUT_FREQ_THRESHOLD:
        del output_vocab[key]
        tag = pos_tag([key])
        if tag[0][1]=='NN' or tag[0][1]=='FW':
            if '<NN>' in output_vocab:
                output_vocab['<NN>']+=1
            else:
                output_vocab['<NN>']=1
            speech_tags[key] = '<NN>'
        elif (tag[0][1] =='CD'):
            if '<CD>' in output_vocab:
                output_vocab['<CD>']+=1
            else:
                output_vocab['<CD>']=1
            speech_tags[key] = '<CD>'

def transform(sentence,vocab):
    sent_tokens = sentence.split(' ')
    print(sentence)
    print(sent_tokens)
    for i in range(0,len(sent_tokens)):
        if sent_tokens[i] not in vocab:
            if sent_tokens[i] in speech_tags:
                sent_tokens[i] = speech_tags[sent_tokens[i]]
    return ' '.join(sent_tokens)
    

for i in range(0,len(train_data)):
    train_data[i] = (transform(train_data[i][0],input_vocab),transform(train_data[i][1],output_vocab))

for i in range(0,len(test_data)):
    test_data[i] = (transform(test_data[i][0],input_vocab),transform(test_data[i][1],output_vocab))

for i in range(0,len(validation_data)):
    validation_data[i] = (transform(validation_data[i][0],input_vocab),transform(validation_data[i][1],output_vocab))


with open(INPUT_VOCAB_FILE,'w',encoding='utf-8') as input_file :
    for key in input_vocab:
        input_file.write(key + " " + str(input_vocab[key]) + "\n")

with open(OUTPUT_VOCAB_FILE,'w',encoding='utf-8') as output_file :
    for key in output_vocab:
        output_file.write(key + " " + str(output_vocab[key]) + "\n")

            
with open(TRAIN_FILE,'w',encoding='utf-8') as train_file :
    for pair in train_data:
        train_file.write(pair[0] + " " + pair[1] + "\n")

with open(TEST_FILE,'w',encoding='utf-8') as test_file :
    for pair in test_data:
        test_file.write(pair[0] + " " + pair[1] + "\n")

with open(VALIDATION_FILE,'w',encoding='utf-8') as validn_file :
    for pair in validation_data:
        validn_file.write(pair[0] + " " + pair[1] + "\n")


