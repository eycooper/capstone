# Teacher Mindfulness Analysis

MSDS Capstone Project Spring 2023

Repo Contents:
- [**audio_transcription**](https://github.com/eycooper/capstone/tree/main/audio_transcription): the code here was used to test out a few APIs to transcribe the videos. However, the sample transcriptions from this method were not very accurate so this approach was not used in the end. Instead [Temi](https://www.temi.com/) was used to transcribe the audio files, providing transcription, speaker labels, and timestamps. 
- [**speech_features**](https://github.com/eycooper/capstone/tree/main/speech_features): extraction and analysis of speech/audio features
  - [Audio_Feature_Engineering.ipynb](https://github.com/eycooper/capstone/blob/main/speech_features/Audio_Feature_Engineering.ipynb): jupyter notebook used to extract speech/audio and some transcript features. This notebook calls the functions defined in the .py file. 
  - [speech_feature_extraction.py](https://github.com/eycooper/capstone/blob/main/speech_features/speech_feature_extraction.py): python file with functions used to extract/engineer speech features.
  - [my-voice-analysis](https://github.com/eycooper/capstone/tree/main/speech_features/my-voice-analysis): contains code from [python my-voice-analysis library](https://github.com/Shahabks/my-voice-analysis) used to extract some speech features. Pip install was not working as expected so copied the library's contents here and made some minor changes to the code to get it to run without errors. Also added [additional file](https://github.com/eycooper/capstone/blob/main/speech_features/myspsolution.praat) from the my-voice-analysis GitHub to run the code.
  - [Archive](https://github.com/eycooper/capstone/tree/main/speech_features/Archive): archive jupyter notebooks from initial code development and testing. Final functions from these files were moved into the speech_feature_extraction.py file. 
  - [Capstone_Audio_EDA.ipynb](https://github.com/eycooper/capstone/blob/main/speech_features/Capstone_Audio_EDA.ipynb): jupyter notebook with exploratory analysis of speech features
