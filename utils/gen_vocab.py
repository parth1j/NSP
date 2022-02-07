import csv
import os
from nlp_utils import NLPUtils
import spacy

nlp = spacy.load("en_core_web_sm")
print("loaded")

FILES = [
    r'C:\Users\admin\Desktop\Sent2LogicalForm\data\train.csv',
    r'C:\Users\admin\Desktop\Sent2LogicalForm\data\test.csv'
]

NAMES = ['train','test']

SQL_VOCAB = ['select','table','from','where','count','min','max','date','year']
POS_TAGS = ['NOUN','NUM','ADJ','PROPN']

INPUT_VOCAB_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\input_vocab.txt'
OUTPUT_VOCAB_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\output_vocab.txt'
TRAIN_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\train.txt'
TEST_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\test.txt'

input_vocab = {}
output_vocab = {}
train_data=[]
test_data=[]
index=0

def transform(sentence):
    sent_tokens = sentence.split(" ")
    temp_arr=[]
    for i in range(0,len(sent_tokens)-1):
        if sent_tokens[i]==sent_tokens[i+1] :
            continue
        else :
            temp_arr.append(sent_tokens[i])
    temp_arr.append(sent_tokens[len(sent_tokens)-1])
    return ' '.join(temp_arr)

for i in range(0,len(FILES)):
    with open(FILES[i], encoding="utf8") as csv_file :
        reader = csv.reader(csv_file)
        next(reader)  # skip header
        index=0
        for row in reader:
            sentence = row[0]
            sent_lower = NLPUtils.to_lower(sentence,True)
            sent_tokens = nlp(sent_lower)
            sentence = ""
            for token in sent_tokens:
                if token.pos_ in POS_TAGS and token.lemma_ not in SQL_VOCAB:
                    if token.pos_ in input_vocab:
                        input_vocab[token.pos_]+=1
                    else:
                        input_vocab[token.pos_]=1
                    sentence = sentence + token.pos_ + " "
                else :
                    if token.lemma_ in input_vocab:
                        input_vocab[token.lemma_]+=1
                    else:
                        input_vocab[token.lemma_]=1
                    sentence = sentence + token.lemma_ + " "
            sql = row[1]
            sent_lower = NLPUtils.to_lower(sql,True)
            sent_tokens = nlp(sent_lower)
            sql = ""
            for token in sent_tokens:
                if token.pos_ in POS_TAGS and token.lemma_ not in SQL_VOCAB:
                    if token.pos_ in output_vocab:
                        output_vocab[token.pos_]+=1
                    else:
                        output_vocab[token.pos_]=1
                    sql = sql + token.pos_ + " "
                else :
                    if token.lemma_ in output_vocab:
                        output_vocab[token.lemma_]+=1
                    else:
                        output_vocab[token.lemma_]=1
                    sql = sql + token.lemma_ + " "
            if NAMES[i]=='train' :
                train_data.append((transform(sentence),transform(sql)))
            elif NAMES[i]=='test' :
                test_data.append((transform(sentence),transform(sql)))
            print(index)
            index+=1
            if(index==100):
                break

input_vocab = dict(sorted(input_vocab.items(), key=lambda item: item[1]))
output_vocab = dict(sorted(output_vocab.items(), key=lambda item: item[1]))


with open(INPUT_VOCAB_FILE,'w',encoding='utf-8') as input_file :
    input_file.truncate(0)
    for key in input_vocab:
        input_file.write(key + " " + str(input_vocab[key]) + "\n")

with open(OUTPUT_VOCAB_FILE,'w',encoding='utf-8') as output_file :
    output_file.truncate(0)
    for key in output_vocab:
        output_file.write(key + " " + str(output_vocab[key]) + "\n")
            
with open(TRAIN_FILE,'w',encoding='utf-8') as train_file :
    train_file.truncate(0)
    for pair in train_data:
        train_file.write(pair[0] + "   " + pair[1] + "\n")

with open(TEST_FILE,'w',encoding='utf-8') as test_file :
    test_file.truncate(0)
    for pair in test_data:
        test_file.write(pair[0] + "   " + pair[1] + "\n")


