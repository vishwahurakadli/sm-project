from toxicClassifier.config.configuration import ConfigurationManager
from toxicClassifier.components.data_validation import DataValidation
from toxicClassifier.logging import logger


class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_ingestion = DataValidation(config=data_validation_config)
        data_ingestion.validate_files()
        