import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.layers import Bidirectional, GlobalMaxPool1D
from keras.models import Model

from toxicClassifier.entity import ModelEvaluationConfig



    
class ModelInference:
    def __init__(self, tokenizer: Tokenizer, embedding_matrix, model_path, maxlen=100):
        self.maxlen = maxlen
        self.tokenizer = tokenizer
        self.embedding_matrix = embedding_matrix
        self.model = None
        self.model_path = model_path
        self.max_features = 20000
        self.embed_size = 50

    def build_model(self):
        inp = Input(shape=(self.maxlen,))
        x = Embedding(self.max_features, self.embed_size, weights=[self.embedding_matrix])(inp)
        x = Bidirectional(LSTM(50, return_sequences=True))(x)
        x = GlobalMaxPool1D()(x)
        x = Dense(50, activation="relu")(x)
        x = Dropout(0.1)(x)
        x = Dense(6, activation="sigmoid")(x)
        model = Model(inputs=inp, outputs=x)
        return model

    def load_trained_model(self):
        self.model = self.build_model()
        self.model.load_weights(self.model_path)

    def preprocess_text(self, texts):
        X = self.tokenizer.texts_to_sequences(texts)
        X = pad_sequences(X, maxlen=self.maxlen)
        return X

    def predict(self, texts):
        X = self.preprocess_text(texts)
        predictions = self.model.predict(X)
        return predictions
