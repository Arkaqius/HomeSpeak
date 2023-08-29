'''
Module to keep NER config
'''
# Path to the trained model directory
PATH_TRAINED_MODEL = "./src/NLP/NER/modelTraining/trainedModel"

# Path to the test sentences file
PATH_TEST_SENTENCES = "./src/NLP/NER/modelTraining/rawDataSet/sentances.txt"

# Path to the training data file in JSON format
PATH_TRAIN_DATA = "./src/NLP/NER/modelTraining/rawDataSet/spacy_training_data_generated.json"

# Path to the vocabulary directory
PATH_VOCAB = './src/NLP/NER/vocab/en-us'

# The size of the training dataset
SIZE_OF_TRAIN_DATA = 3000

# The number of epochs for training the model
NUMBER_OF_EPOCHS = 50

# The train-validation data ratio
TRAIN_VAL_RATION = 0.7
