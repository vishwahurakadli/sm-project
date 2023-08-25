from toxicClassifier.entity import ModelTrainerConfig

import os

import numpy as np
import pandas as pd
import pickle
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.layers import Bidirectional, GlobalMaxPool1D
from keras.models import Model



class ModelTrainer:
    def __init__(self, embed_file, maxlen=100, embed_size=50, max_features=20000):
        self.maxlen = maxlen
        self.embed_file =  embed_file
        self.embed_size = embed_size
        self.max_features = max_features

    @staticmethod
    def get_coefs(word,*arr):
        return word, np.asarray(arr, dtype='float32')

    def load_embedding(self):
        embeddings_index = dict(self.get_coefs(*o.strip().split()) for o in open(self.embed_file, encoding='utf-8'))
        all_embs = np.stack(list(embeddings_index.values()))
        emb_mean, emb_std = all_embs.mean(), all_embs.std()
        word_index = self.tokenizer.word_index
        nb_words = min(self.max_features, len(word_index))
        embedding_matrix = np.random.normal(emb_mean, emb_std, (nb_words, self.embed_size))
        # print("token words",len(word_index))
        for word, i in word_index.items():
            if i>= self.max_features: continue
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None: embedding_matrix[i] = embedding_vector
        return embedding_matrix
    
    def build_model(self):
        inp = Input(shape=(self.maxlen,))
        x = Embedding(self.max_features, self.embed_size, weights=[self.embedding_matrix])(inp)
        x = Bidirectional(LSTM(50,return_sequences=True))(x)
        x = GlobalMaxPool1D()(x)
        x = Dense(50, activation="relu")(x)
        x = Dropout(0.1)(x)
        x = Dense(6, activation="sigmoid")(x)
        model = Model(inputs=inp, outputs=x)
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model = model
        return model
    
    def train(self, X, Y, batch_size=32, epochs=2):
        self.tokenizer = Tokenizer(num_words=self.max_features)
        self.tokenizer.fit_on_texts(X)
        X = self.tokenizer.texts_to_sequences(X)
        X = pad_sequences(X, maxlen=self.maxlen)
        self.embedding_matrix = self.load_embedding()
        self.model = self.build_model()
        self.model.fit(X, Y, batch_size=batch_size, epochs=epochs)
