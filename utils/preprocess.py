import csv
import os
from nlp_utils import NLPUtils

FILES = [
    r'C:\Users\admin\Desktop\Sent2LogicalForm\data\train.csv',
    r'C:\Users\admin\Desktop\Sent2LogicalForm\data\test.csv',
    r'C:\Users\admin\Desktop\Sent2LogicalForm\data\validation.csv'
]

NAMES = ['train','test','validation']

INPUT_VOCAB_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\input_vocab_p.txt'
OUTPUT_VOCAB_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\output_vocab_p.txt'
TRAIN_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\train_p.txt'
TEST_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\test_p.txt'
VALIDATION_FILE = r'C:\Users\admin\Desktop\Sent2LogicalForm\data\validation_p.txt'

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
        index=0
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
            if(index==2000):
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

with open(VALIDATION_FILE,'w',encoding='utf-8') as validn_file :
    validn_file.truncate(0)
    for pair in validation_data:
        validn_file.write(pair[0] + "   " + pair[1] + "\n")


