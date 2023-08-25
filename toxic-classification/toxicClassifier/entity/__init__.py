from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    data_dir: Path
    local_data_file: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    data_path: Path
    glove_path: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    data_path: Path
    models_dir: Path
    embed_file: Path
    model_path: Path
    tokenizer_path: Path
    embed_mat: Path
    validation_path: Path




@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    data_path: Path
    model_path: Path
    tokenizer_path: Path
    embed_mat: Path
    validation_path: Path
    validation_output: Path
    confusion_matrix_path: Path