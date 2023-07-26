# About module
__name__ = "VoiceHAC_NER_module"
__doc__ = """
The VoiceHAC NER (Named Entity Recognition) module is responsible for parsing utterances 
to identify entities such as names, locations, and things. This is an integral part of 
understanding the user's intent in their command.

The module is organized as follows:

- NER Processing: This component processes natural language text, identifies entities,
  classifies them into pre-determined categories such as 'person', 'location', 'thing', etc.

Main features:
1) Entity recognition and classification: It can recognize named entities in the text, 
   and classify them into their appropriate categories.
2) Supporting the understanding of user's intent: By identifying the entities in a user's 
   command, it provides crucial context that aids in understanding the user's intent.
   
Please note, this module is part of a larger system and is designed to work in conjunction 
with the other components of the VoiceHAC system.
"""
__author__ = "Arkaqius"  # The author of this module
__version__ = "v1.0.0"  # The current version of this module
