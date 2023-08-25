from toxicClassifier.config.configuration import ConfigurationManager
from toxicClassifier.logging import logger
from toxicClassifier.components.model_evaluation import ModelInference
import pickle
import json
from toxicClassifier.components.youtube_comments import get_comments


class PredictionPipeline:
    def __init__(self):
        self.config = ConfigurationManager().get_model_evaluation_config()


    
    def predict(self,video_id):
        logger.info(f"Prediction started !!")
        with open(self.config.tokenizer_path, 'rb') as handle:
            tokenizer = pickle.load(handle)
        with open(self.config.embed_mat, 'rb') as handle:
            embedding_matrix = pickle.load(handle)
        try:
            pipe = ModelInference(tokenizer=tokenizer, embedding_matrix=embedding_matrix, model_path=self.config.model_path)
            pipe.load_trained_model()
            logger.info(f"Model loaded successfully !!")
        except Exception as e:
            logger.error(f"Model loading failed !! {e}")
            raise Exception(f"Model loading failed !! {e}")

        try:
            comments=get_comments(video_id)
            logger.info(f"Comments fetched successfully !!")
        except Exception as e:
            logger.error(f"Comments fetching failed !! {e}")
            raise Exception(f"Comments fetching failed !! {e}") 

        try:
            output = pipe.predict(comments)
            logger.info(f"Prediction completed successfully !!") 
        except Exception as e:
            logger.error(f"Prediction failed !! {e}")
            raise Exception(f"Prediction failed !! {e}")


        toxic_comments = [[comments[i],output[i][0]] for i in range(len(output)) if output[i][0] >= 0.5]
        toxic_comments = sorted(toxic_comments, key=lambda x: x[1], reverse=True)[:10]
        toxic_comments = [i[0] for i in toxic_comments]

        pred_labels = [1 if i >= 0.5 else 0 for i in output[:, 0]]
    
        result = {'toxic': sum(pred_labels), 
                  'non-toxic': len(pred_labels) -sum(pred_labels), 
                  'toxic_comments': toxic_comments}



        result_log = json.dumps(result, indent=4)
        # only write the result to log file not to console
        logger.info(f"Prediction result for {video_id} : {result_log}")
        # logger.info(f"Prediction result for {video_id} : {result_log.decode('utf16')}")
        return result