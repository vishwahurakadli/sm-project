from toxicClassifier.config.configuration import ConfigurationManager
from toxicClassifier.components.model_trainer import ModelTrainer
from toxicClassifier.logging import logger
import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split

class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(embed_file=model_trainer_config.embed_file)
        data = pd.read_csv(model_trainer_config.data_path)
        data['comment_text'].fillna("fillna")
        y_label = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
        x_train, x_test, y_train, y_test = train_test_split(data['comment_text'], data[y_label], test_size=0.2, random_state=42)
        model_trainer.train(x_train, y_train, batch_size=32, epochs=2)

        os.makedirs(model_trainer_config.models_dir, exist_ok=True)
        logger.info(f"Model training completed successfully !!")
        with open(model_trainer_config.tokenizer_path, 'wb') as handle:
            pickle.dump(model_trainer.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(model_trainer_config.embed_mat, 'wb') as handle:
            pickle.dump(model_trainer.embedding_matrix, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info(f"Tokenizer and embedding matrix saved successfully !!")

        model_trainer.model.save_weights(model_trainer_config.model_path)

        logger.info(f"Model saved successfully !!")

        validation = y_test
        validation['comment_text'] = x_test
        validation.to_csv(model_trainer_config.validation_path, index=False)