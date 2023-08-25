import os
from toxicClassifier.config.configuration import ConfigurationManager
from toxicClassifier.logging import logger
from pathlib import Path
from toxicClassifier.entity import DataValidationConfig
from datasets import load_dataset



class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    
    def validate_files(self):
        # check each directpry and files exist or not using config
        # if not exist then create the directory and raise the error

        if not os.path.exists(self.config.root_dir):
            raise FileNotFoundError(f"Root directory not found at {self.config.root_dir}")
        if not os.path.exists(self.config.data_path):
            raise FileNotFoundError(f"Data directory not found at {self.config.data_path}")
        if not os.path.exists(self.config.glove_path):
            raise FileNotFoundError(f"Glove directory not found at {self.config.glove_path}")
        
        logger.info("All the directories and files are present")
        
