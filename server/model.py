import torch
import torch.nn as nn
import torch.nn.functional as F

device="cpu"

class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EncoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size,num_layers=1)

    def forward(self, input,context, hidden):
        embedded = self.embedding(input).view(1, 1, -1)
        output = embedded
        output, (hidden,context) = self.lstm(output,(hidden,context))
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)

class AttnDecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size, dropout_p=0.1, max_length=5000):
        super(AttnDecoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.dropout_p = dropout_p
        self.max_length = max_length

        self.embedding = nn.Embedding(self.output_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
        self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)
        self.lstm = nn.LSTM(self.hidden_size, self.hidden_size,num_layers=1)
        self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input,context, hidden, encoder_outputs):
        embedded = self.embedding(input).view(1, 1, -1)
        embedded = self.dropout(embedded)
        attn_weights = F.softmax(self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
        attn_applied = torch.bmm(attn_weights.unsqueeze(0),encoder_outputs.unsqueeze(0))
        output = torch.cat((embedded[0], attn_applied[0]), 1)
        output = self.attn_combine(output).unsqueeze(0)
        output = F.relu(output)
        output,(hidden,context) = self.lstm(output,(hidden,context))
        output = F.log_softmax(self.out(output[0]), dim=1)
        return output,(hidden,context), attn_weights

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)


def getSavedModel(encoder_path,decoder_path,input_lang,output_lang,device) :
    hidden_size = 256
    encoder = EncoderRNN(input_lang.n_words, hidden_size).to(device)
    attn_decoder = AttnDecoderRNN(hidden_size,output_lang.n_words, dropout_p=0.1).to(device)
    encoder.load_state_dict(torch.load(encoder_path,map_location=torch.device(device)))
    attn_decoder.load_state_dict(torch.load(decoder_path,map_location=torch.device(device)))
    return encoder,attn_decoder