# About module
__name__ = "VoiceHAC - Natural language processing"
__author__ = "Arkaqius"
__version__ = "v1.1.0"
__doc__ = """
The VoiceHAC module is designed for processing natural language commands 
and delegating these commands to the appropriate skills for execution.

The module is organized as follows:

- Natural Language Processing (NLP): This component of the module takes 
  in natural language text and analyzes it for commands and intents.
  
- Skills: These are the capabilities of the module. When the NLP component 
  identifies a command, it is sent to the appropriate skill for execution. 
  For example, a command to control lights would be sent to a light control skill.

This module is currently in development and will be expanded with additional 
capabilities and skills over time.

Main features:
1) Natural language command processing: The NLP component can identify commands 
   from natural language text.
2) Skill execution: Identified commands are executed using the relevant skills.
"""
