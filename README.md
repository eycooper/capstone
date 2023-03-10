# Teacher Mindfulness Analysis

## MSDS Capstone Project Spring 2023
- Students: Kaia Lindberg, Grace Lyons, Emma Cooper, Tulsi Ratnam
- Sponsor: Tara Hofkens
- Mentor: Abbas Kazemipour

Repo Contents:
- [**speech_features**](https://github.com/eycooper/capstone/tree/main/speech_features): extraction and analysis of speech/audio features
  - [speech_features_documentation.md](https://github.com/eycooper/capstone/blob/main/speech_features/speech_features_documentation.md): documentation on methods for extracting features from audio data.
  - [Audio_Features_Comparing_Groups.ipynb](https://github.com/eycooper/capstone/blob/main/speech_features/Audio_Features_Comparing_Groups.ipynb): preliminary analysis with t-tests and visualization comparing some features between the treatment and control groups.
  - [Capstone_Audio_EDA.ipynb](https://github.com/eycooper/capstone/blob/main/speech_features/Capstone_Audio_EDA.ipynb): jupyter notebook with exploratory analysis of speech features.
  - [Audio_Feature_Engineering.ipynb](https://github.com/eycooper/capstone/blob/main/speech_features/Audio_Feature_Engineering.ipynb): jupyter notebook used to extract speech/audio and some transcript features. This notebook calls the functions defined in the .py file. 
  - [speech_feature_extraction.py](https://github.com/eycooper/capstone/blob/main/speech_features/speech_feature_extraction.py): python file with functions used to extract/engineer speech features.
  - [my-voice-analysis](https://github.com/eycooper/capstone/tree/main/speech_features/my-voice-analysis): contains code from [python my-voice-analysis library](https://github.com/Shahabks/my-voice-analysis) used to extract some speech features. Pip install was not working as expected so copied the library's contents here and made some minor changes to the code to get it to run without errors. Also added [additional file](https://github.com/eycooper/capstone/blob/main/speech_features/myspsolution.praat) from the my-voice-analysis GitHub to run the code.
  - [Archive](https://github.com/eycooper/capstone/tree/main/speech_features/Archive): archive jupyter notebooks from initial code development and testing. Final functions from these files were moved into the speech_feature_extraction.py file. 
- [**audio_transcription**](https://github.com/eycooper/capstone/tree/main/audio_transcription): the code here was used to test out a few APIs to transcribe the videos. However, the sample transcriptions from this method were not very accurate so this approach was not used in the end. Instead [Temi](https://www.temi.com/) was used to transcribe the audio files, providing transcription, speaker labels, and timestamps. 
