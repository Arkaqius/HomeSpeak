import os
from enum import Enum
import config as cfg

def generate_enum_from_files(directory: str, enum_name: str) -> Enum:
    # Get the list of files in the directory
    files = os.listdir(directory)

    # Remove file extensions (assuming they are .py files)
    names = [os.path.splitext(file)[0] for file in files if file.endswith(".voc")]

    # Create the enum
    return Enum(enum_name, {name.upper(): name for name in names})


Things = generate_enum_from_files(os.path.join(cfg.PATH_VOCAB,'things') , 'Things')
Actions = generate_enum_from_files(os.path.join(cfg.PATH_VOCAB,'actions') , 'Actions')
Attributes = generate_enum_from_files(os.path.join(cfg.PATH_VOCAB,'attributes') , 'Attributes')
Locations = generate_enum_from_files(os.path.join(cfg.PATH_VOCAB,'location') , 'Locations')
States = generate_enum_from_files(os.path.join(cfg.PATH_VOCAB,'states') , 'States')