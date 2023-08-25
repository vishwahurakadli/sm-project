from toxicClassifier.constants import *
from toxicClassifier.utils.common import read_yaml, create_directories
from toxicClassifier.entity import (DataIngestionConfig,
                                   DataValidationConfig,
                                   ModelTrainerConfig,
                                   ModelEvaluationConfig)


class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            data_dir=config.data_dir,
            local_data_file=config.local_data_file,
        )

        return data_ingestion_config
    


    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            glove_path=config.glove_path,
        )

        return data_validation_config
    


    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.TrainingArguments

        # create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            embed_file=config.embed_file,
            models_dir=config.models_dir,
            model_path=config.model_path,
            tokenizer_path=config.tokenizer_path,
            embed_mat=config.embed_mat,    
            validation_path=config.validation_path,       
        )

        return model_trainer_config
    

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation

        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            model_path = config.model_path,
            tokenizer_path = config.tokenizer_path,
            embed_mat = config.embed_mat,
            validation_path=config.validation_path,       
            validation_output=config.validation_output,    
            confusion_matrix_path=config.confusion_matrix_path,
        )

        return model_evaluation_config
