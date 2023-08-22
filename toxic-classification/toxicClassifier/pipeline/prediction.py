from toxicClassifier.config.configuration import ConfigurationManager
from toxicClassifier.logging import logger
from toxicClassifier.components.model_evaluation import ModelInference
import pickle
from toxicClassifier.components.youtube_comments import get_comments


class PredictionPipeline:
    def __init__(self):
        self.config = ConfigurationManager().get_model_evaluation_config()


    
    def predict(self,video_id):
        
        with open(self.config.tokenizer_path, 'rb') as handle:
            tokenizer = pickle.load(handle)
        with open(self.config.embed_mat, 'rb') as handle:
            embedding_matrix = pickle.load(handle)
        pipe = ModelInference(tokenizer=tokenizer, embedding_matrix=embedding_matrix, model_path=self.config.model_path)
        pipe.load_trained_model()

        print("Dialogue:")
        print(video_id)
        comments=get_comments(video_id) 
        output = pipe.predict(comments)
        print(output)
        toxic_comments = [[comments[i],output[i][0]] for i in range(len(output)) if output[i][0] >= 0.5]
        toxic_comments = sorted(toxic_comments, key=lambda x: x[1], reverse=True)[:10]
        toxic_comments = [i[0] for i in toxic_comments]
        print(toxic_comments)
        pred_labels = [1 if i >= 0.5 else 0 for i in output[:, 0]]
        # y_label = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
        # result = {y_label[i]:round(float(output[i]),4) for i in range(len(y_label))}
        result = {'toxic': sum(pred_labels), 'non-toxic': len(pred_labels) -sum(pred_labels)}
        return result