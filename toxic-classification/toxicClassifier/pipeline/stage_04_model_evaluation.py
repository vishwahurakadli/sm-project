from toxicClassifier.config.configuration import ConfigurationManager
from toxicClassifier.components.model_evaluation import ModelInference
from toxicClassifier.logging import logger
import pandas as pd
import pickle
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report, accuracy_score, f1_score, precision_score, recall_score
import seaborn as sns
import matplotlib.pyplot as plt
from toxicClassifier.utils.common import create_directories
import json



class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        validation = pd.read_csv(model_evaluation_config.validation_path)
        x_val = validation['comment_text']
        y_label = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
        y_val = validation[y_label]
        with open(model_evaluation_config.tokenizer_path, 'rb') as handle:
            tokenizer = pickle.load(handle)
        with open(model_evaluation_config.embed_mat, 'rb') as handle:
            embedding_matrix = pickle.load(handle)
        model_evaluation = ModelInference(tokenizer=tokenizer, embedding_matrix=embedding_matrix, model_path=model_evaluation_config.model_path)
        model_evaluation.load_trained_model()
        predictions = model_evaluation.predict(x_val)
        # classify the scores into 0 and 1 using threshold 0.5 here predictions in 2d list
        validation_results = dict()
        logger.info(f"Model evaluation started !!")
        roc_auc_score_list = []
        accuracy_score_list = []
        f1_score_list = []
        precision_score_list = []
        recall_score_list = []
        for i, j in enumerate(y_label):
            logger.info(f"{j} roc_auc_score: \n{roc_auc_score(y_val[j], predictions[:, i])}")
            roc_auc_score_list.append(roc_auc_score(y_val[j], predictions[:, i]).round(2))

        predictions[predictions>=0.5] = 1
        predictions[predictions<0.5] = 0
        for i, j in enumerate(y_label):
            logger.info(f"{j} accuracy_score: \n{accuracy_score(y_val[j], predictions[:, i].round(2))}")
            accuracy_score_list.append(accuracy_score(y_val[j], predictions[:, i].round(2)))
            logger.info(f"{j} f1_score: \n{f1_score(y_val[j], predictions[:, i].round(2))}")
            f1_score_list.append(f1_score(y_val[j], predictions[:, i].round(2)))
            logger.info(f"{j} precision_score: \n{precision_score(y_val[j], predictions[:, i].round(2))}")
            precision_score_list.append(precision_score(y_val[j], predictions[:, i].round(2)))
            logger.info(f"{j} recall_score: \n{recall_score(y_val[j], predictions[:, i].round(2))}")
            recall_score_list.append(recall_score(y_val[j], predictions[:, i].round(2)))
    
        validation_results['accuracy_score'] = accuracy_score_list
        validation_results['f1_score'] = f1_score_list
        validation_results['precision_score'] = precision_score_list
        validation_results['recall_score'] = recall_score_list
        validation_results['roc_auc_score'] = roc_auc_score_list

        create_directories([model_evaluation_config.confusion_matrix_path])
        folder_path = model_evaluation_config.confusion_matrix_path + '/'
        for i, j in enumerate(y_label):
            logger.info(f"{j} classification_report: \n{classification_report(y_val[j], predictions[:, i])}")
            logger.info(f"{j} confusion_matrix: \n{confusion_matrix(y_val[j], predictions[:, i])}")
            sns.heatmap(confusion_matrix(y_val[j], predictions[:, i]), annot=True, fmt='d')
            plt.xticks
            plt.savefig(f"{folder_path}_{j}.png")
            plt.clf()

        # save the validation results dict to json file
        logger.info(f"Validation results: \n{validation_results}")
        with open(model_evaluation_config.validation_output, 'w') as fp:
            json.dump(validation_results, fp, indent=4)

        logger.info(f"Model evaluation completed successfully !!")

        