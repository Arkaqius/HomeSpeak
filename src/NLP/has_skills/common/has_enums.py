# pylint: disable=C0114
import os
from enum import Enum
import ner.config as cfg


def generate_enum_from_files(directory: str, enum_name: str) -> Enum:
    """
    Generate a Python Enum class from the files in the specified directory.

    Args:
        directory (str): The path to the directory containing the files.
        enum_name (str): The desired name for the Enum class.

    Returns:
        Enum: An Enum class with keys derived from the file names in the directory.
    """
    # Check if path is valid
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")

    # Get the list of files in the directory
    files = os.listdir(directory)

    # Remove file extensions (assuming they are .voc files)
    names = [os.path.splitext(file)[0]
             for file in files if file.endswith(".voc")]

    # Check if voc files are present
    if not names:
        raise ValueError(f"No .voc files found in the directory {directory}.")

    # Check if names in voc files are valid Python names
    for name in names:
        if not name.isidentifier():
            raise ValueError(f"'{name}' is not a valid Python identifier.")

    # Create the enum
    return Enum(enum_name, {name.upper(): name for name in names})


# Generate Enums based on files in the respective directories
Things = generate_enum_from_files(
    os.path.join(cfg.PATH_VOCAB, "things"), "Things")
Actions = generate_enum_from_files(
    os.path.join(cfg.PATH_VOCAB, "actions"), "Actions")
Attributes = generate_enum_from_files(
    os.path.join(cfg.PATH_VOCAB, "attributes"), "Attributes"
)
Locations = generate_enum_from_files(
    os.path.join(cfg.PATH_VOCAB, "location"), "Locations"
)
States = generate_enum_from_files(
    os.path.join(cfg.PATH_VOCAB, "states"), "States")
