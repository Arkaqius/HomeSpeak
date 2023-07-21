
from .modelTraining import generateRawData
from .modelTraining import trainModel
from .modelTraining import NER_test

# About module
__name__ = "VoiceHAC NER module"
__doc__ = "VoiceHAC naming entity recognization module. Parse utterence to know entities names, locations, things etc."
__author__ = "Arkaqius"
__version__ = "v0.1.0"


def generateTrainData()-> None :
    generateRawData()

def trainNERModel()-> None:
    trainModel()

def trainNERModel()-> None:
    NER_test()