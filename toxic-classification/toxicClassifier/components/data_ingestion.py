import os
from toxicClassifier.config.configuration import ConfigurationManager
from toxicClassifier.logging import logger
from pathlib import Path
from toxicClassifier.entity import DataIngestionConfig
from datasets import load_dataset



class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    
    def download_file(self):
        if not os.path.exists(self.config.data_dir):
            os.makedirs(self.config.data_dir)
        if not os.path.exists(self.config.local_data_file):
            dat = load_dataset("tasksource/jigsaw")
            df = dat['train'].to_pandas()
            df.to_csv(self.config.local_data_file, index=False)
            logger.info(f"File downloaded at {self.config.local_data_file}")
        else:
            logger.info(f"File already exists at {self.config.local_data_file}")  

    