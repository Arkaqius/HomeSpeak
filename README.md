# Blog

Project is maintened and described in my [blog](arekdevdiary.wordpress.com). Check it!

# VoiceHAC

VoiceHAC (Voice Home Automation Controller) is a comprehensive solution for controlling smart home devices through natural language processing. The project uses custom-trained NER models to understand voice commands, enabling users to control various aspects of their smart home environment.  

## VoiceHAC-NER

VoiceHAC-NER (Voice Home Automation Controller - Named Entity Recognition) is a project that uses natural language processing techniques to parse and understand voice commands for controlling smart home devices. The project leverages a custom-trained named entity recognition model using the SpaCy library to identify relevant entities in the given text.  

### Features

- Custom-trained NER model to recognize home automation-related entities
- Named entity recognition for actions, attributes, things, and locations
- Extract numerical values, including fractions and percentages

### Installation

1. Install the required dependencies with `pip`:

\```sh
pip install -r requirements.txt
\```

2. Download and install the pre-trained SpaCy model (if not already installed):

\```sh
python -m spacy download en_core_web_sm
\```

3. Configure the paths in `config.py` to point to your trained model and test sentences file.

### Usage

Import the `VoiceHAC_NER` class in your Python script or application, and use it to process text commands:

\```python
from voicehac_ner import VoiceHAC_NER

ner = VoiceHAC_NER(model_path)
entities = ner.get_named_entities(text)
numbers = ner.extract_numerical_values(text)
\```

Replace `model_path` with the path to your custom-trained model, and `text` with the input command.

### License

This project is licensed under the MIT License.


