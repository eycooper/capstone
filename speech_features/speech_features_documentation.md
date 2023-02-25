# Speech/Audio Feature Descriptions

This file contain information about the various speech, audio, and transcript features that were generated for analysis in [Audio_Feature_Engineering.ipynb](https://github.com/eycooper/capstone/blob/main/speech_features/Audio_Feature_Engineering.ipynb).


## Overall Process
The features described in this file were engineered using the Temi transcripts, speaker labels, and audio files. First, the Temi transcripts were manually reviewed to identify which [speaker label](https://github.com/eycooper/capstone/blob/main/speaker_identification.xlsx) corresponds to the teacher in each transcript. The audio files were originally in .m4a format, but were converted to .wav files using [pydub](https://github.com/jiaaro/pydub). The speaker labels, transcript timestamps, and audio files were used to extract just the teacher's audio (i.e. removing the portions of audio where the student avatars were speaking). From there various python libraries, described in detail in the sections below, were used to extract features of interest. 


## Transcript Features 
Some features were engineered from the Temi transcripts. Using information like the speaker labels, timestamps, and high level text information. More thorough text analysis using NLP techniques is done in the [text_analytics_code](https://github.com/eycooper/capstone/tree/main/text_analytics_code) section. The goal here was explore some simple features such as speaking duration, word count, and speaker changes. These features could be used to analyze the frequency of student interruptions, speed of speech, and balance of talking between teacher and students.

Some of the features were extracted include:
- Duration including duration in seconds (total, teacher, and student), average duration (total, teacher, and student), and percent of the time that the teacher is the speaker.
- Word count including total count (total, teacher, and student), percent of words said by teacher, and word rate (total, teacher, and student).
- Line count (aka number of changes in speakers) including number of speaker changes (total line count) and number of time student/teacher speaks (student/teacher line count).

Variable Descriptions:
- Total_Duration: total speaking duration in seconds
- Teacher_Duration: speaking duration of teacher in seconds
- Student_Duration: speaking duration of the students/avatars in seconds
- Percent_Time_Teacher: percent of total time that the teacher is talking (Teacher_Duration/Total_Duration)
- Average_Speaker_Duration: average length of speaking duration (Total_Duration/Total_Lines)
- Average_Teacher_Duration: teacher's average length of speaking duration (Teacher_Duration/Teacher_Lines)
- Average_Student_Duration: student's average length of speaking duration (Student_Duration/Student_Lines)
- Total_Word_Count: count of number of words said 
- Teacher_Word_Count: count of number of words said by teacher
- Student_Word_Count: count of number of words said by student
- Teacher_Percent_Words: percent of total words said by teacher (Teacher_Word_Count/Total_Word_Count)
- Total_Word_Rate: overall speaking rate (Total_Word_Count/Total_Duration)
- Teacher_Word_Rate: teacher speaking rate (Teacher_Word_Count/Teacher_Duration)
- Student_Word_Rate: student speaking rate (Student_Word_Count/Student_Duration)
- Total_Speaker_Line_Count: number of changes of speakers
- Teacher_Line_Count: number of times the teacher speaks
- Student_Line_Count: number of times students speak


## Speech/Audio Features

The next set of features were generated using various Python libraries to calculate different speech characteristics from the teacher only audio files. The libraries and features used were inspired by a [study](https://www.jmir.org/2021/4/e24191) analyzing stress of health care professionals via speech analysis. Many of these features are continuous (vary over time) so some aggregation measures (e.g. mean, variance, min, max, etc.) were calculated for analysis of overall averages and variance for each teacher. 

### My-Voice-Analysis Features

The Python [My-Voice-Analysis Library](https://github.com/Shahabks/my-voice-analysis) was used to generate audio features such as balance, pauses, speaking rate, and f0 stats. In order to generate these features this library "breaks utterances and detects syllable boundaries, fundamental frequency contours, and formants". 

Features extracted:
- number_ of_syllables: count of the number of syllables
- number_of_pauses: number of fillers and pauses
- rate_of_speech: speed of speech
- articulation_rate: articulation (speed)
- speaking_duration: speaking time excluding fillers and pauses
- original_duration: total duration including fillers and pauses
- balance: ratio between speaking duration and total duration
- f0: fundamental frequency, the frequency at which vocal cords vibrate, the representation of what is perceived as pitch
    - Various aggregations: mean, standard deviation (std), median, min, max, quantile25, quantile 75)
- Mood: characteristic of mood of speech (e.g. reading, speaking passionately, showing no emotion)



