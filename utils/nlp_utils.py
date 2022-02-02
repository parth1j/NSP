"""TODO"""
import os
import string

# import stanfordnlp
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

PORTER_STEMMER = PorterStemmer()


class NLPUtils:
    """TODO"""

    @staticmethod
    def sentence_tokenization(text):
        """TODO"""
        lines = text.split("\n")
        sentences = []
        for line in lines:
            for sentence in sent_tokenize(line):
                sentences.append(sentence)
        return sentences

    @staticmethod
    def preprocess_sentence(sentence,lower=True):
        sentence = NLPUtils.to_lower(sentence, lower)
        tokens = NLPUtils.word_tokenization(sentence)
        return tokens

    @staticmethod
    def is_ascii(s):
        return all(ord(c) < 128 for c in s)

    @staticmethod
    def has_digit(string):
        return any(char.isdigit() for char in string)

    @staticmethod
    def remove_hyperlinks(text):
        """TODO"""
        import re

        regex = r"((https?:\/\/)?[^\s]+\.[^\s]+)"
        text = re.sub(regex, "", text)
        return text

    @staticmethod
    def stopword_elimination(sentence):
        """TODO"""
        return [word for word in sentence if word not in stopwords.words("english")]

    @staticmethod
    def nonalpha_removal(sentence):
        """TODO"""
        return [word for word in sentence if word.isalpha()]

    @staticmethod
    def nonascii_removal(sentence):
        """TODO"""
        return [
            word
            for word in sentence
            if (NLPUtils.is_ascii(word) and (not (NLPUtils.has_digit(word))))
        ]

    @staticmethod
    def punctuation_removal(token):
        """TODO"""
        d = {w: " " for w in string.punctuation}
        translator = str.maketrans(d)
        return token.translate(translator)

    @staticmethod
    def to_lower(token, lower):
        """TODO"""
        return token.lower() if lower else token

    """
    @staticmethod
    def word_tokenization(sentence):
        doc = NLP(sentence)
        return [token.text for token in doc.sentences[0].tokens]
    """

    @staticmethod
    def word_tokenization(sentence):
        return [token for token in word_tokenize(sentence)]

    @staticmethod
    def dependency_parse(sentence):
        """TODO"""
        doc = NLP(sentence)
        return [dep for dep in doc.sentences[0].dependencies]

    @staticmethod
    def porter_stem(word):
        return PORTER_STEMMER.stem(word)
