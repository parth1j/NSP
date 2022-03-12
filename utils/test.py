'''import spacy

nlp = spacy.load("en_core_web_sm")
print("loaded")
doc = nlp("``")

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
ENCODER_PATH = r'encoder.pth'
DECODER_PATH = r'decoder.pth'
print(device)
'''
import os
path = r"C:\Users\admin\Desktop\Sent2LogicalForm\database"
dir_list = os.listdir(path)
db_files_dict = {}
for dir in dir_list:
    file_list = os.listdir(path + "/" + dir)
    print(file_list) 