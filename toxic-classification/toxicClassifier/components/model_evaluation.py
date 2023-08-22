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



# class ModelEvaluation:
#     def __init__(self, config: ModelEvaluationConfig):
#         self.config = config


    
#     def generate_batch_sized_chunks(self,list_of_elements, batch_size):
#         """split the dataset into smaller batches that we can process simultaneously
#         Yield successive batch-sized chunks from list_of_elements."""
#         for i in range(0, len(list_of_elements), batch_size):
#             yield list_of_elements[i : i + batch_size]

    
#     def calculate_metric_on_test_ds(self,dataset, metric, model, tokenizer, 
#                                batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu", 
#                                column_text="article", 
#                                column_summary="highlights"):
#         article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
#         target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

#         for article_batch, target_batch in tqdm(
#             zip(article_batches, target_batches), total=len(article_batches)):
            
#             inputs = tokenizer(article_batch, max_length=1024,  truncation=True, 
#                             padding="max_length", return_tensors="pt")
            
#             summaries = model.generate(input_ids=inputs["input_ids"].to(device),
#                             attention_mask=inputs["attention_mask"].to(device), 
#                             length_penalty=0.8, num_beams=8, max_length=128)
#             ''' parameter for length penalty ensures that the model does not generate sequences that are too long. '''
            
#             # Finally, we decode the generated texts, 
#             # replace the  token, and add the decoded texts with the references to the metric.
#             decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True, 
#                                     clean_up_tokenization_spaces=True) 
#                 for s in summaries]      
            
#             decoded_summaries = [d.replace("", " ") for d in decoded_summaries]
            
            
#             metric.add_batch(predictions=decoded_summaries, references=target_batch)
            
#         #  Finally compute and return the ROUGE scores.
#         score = metric.compute()
#         return score


#     def evaluate(self):
#         device = "cuda" if torch.cuda.is_available() else "cpu"
#         tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
#         model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)
       
#         #loading data 
#         dataset_samsum_pt = load_from_disk(self.config.data_path)


#         rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
  
#         rouge_metric = load_metric('rouge')

#         score = self.calculate_metric_on_test_ds(
#         dataset_samsum_pt['test'][0:10], rouge_metric, model_pegasus, tokenizer, batch_size = 2, column_text = 'dialogue', column_summary= 'summary'
#             )

#         rouge_dict = dict((rn, score[rn].mid.fmeasure ) for rn in rouge_names )

#         df = pd.DataFrame(rouge_dict, index = ['pegasus'] )
#         df.to_csv(self.config.metric_file_name, index=False)

        

