'''
Functions used to extract speech/audio features for analysis

'''

import os
from pydub import AudioSegment
import wave
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
mysp=__import__('my-voice-analysis')
from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
from scipy.stats import kurtosis, skew
import librosa



'''
Convert Audio Files to Wav Files

'''
def convert_m4a_to_wav(file_name, m4a_path, wav_path):
    '''
    Convert an .m4a audio file to a .wav audio file using PyDub.

    Inputs:
        - file_name (str): name of file (without extension)
        - m4a_path (str): directory path for input .m4a file
        - wav_path (str): directory path for output .wav file

    Returns:
        - saves wav file to wav_path
    '''
    
    try:
        # Load the m4a file
        audio = AudioSegment.from_file(m4a_path + file_name + '.m4a', format = 'm4a')

        # Set the desired sample rate and bit depth
        desired_sample_rate = 44100
        desired_sample_width = 2  # 16-bit depth

        # Resample the audio to the desired sample rate
        resampled_audio = audio.set_frame_rate(desired_sample_rate)

        # Set the bit depth to the desired value
        converted_audio = resampled_audio.set_sample_width(desired_sample_width)

        # Export the converted audio to a new WAV file
        converted_audio.export(wav_path + file_name + '.wav', format="wav")
    
    except:
        print(f'Error converting {file_name}')
    
    



'''
Extract Only Teacher Audio

'''
def extract_teacher_timestamps(file_name, transcript_path, teacher_speaker_num):
    '''
    Create a list of timestamp pairs in between which the teacher is speaking
    
    Inputs:
        - file_name: name of original file
        - transcript_path: directory containing transcripts
        - teacher_speaker_num: integer of which speaker number in the transcript corresponds to the teacher 
    
    Returns:
        - List of timestamp pairs between which the teacher is the speaker
    '''
    
    # Read in transcript
    df = pd.read_csv(transcript_path + file_name + '.txt', 
                 engine = 'python', 
                 delimiter = "                                             ",
                 header = None)
    
    df.columns = ['Speaker', 'Timestamp', 'Text']

    # Create a column that converts the timestamps to seconds
    df['Timestamp_Secs'] = df['Timestamp'].apply(convert_time_to_seconds)
    
    # Create a column with pairs of timestamps
    df['Timestamp_Pairs'] = df.apply(create_timestamp_pairs, col = 'Timestamp_Secs', df = df, axis=1)
    
    # Filter to only the teacher
    df_teacher = df[df['Speaker'] == f'Speaker {teacher_speaker_num}:']
    
    # Get a list of the timestamp pairs
    timestamp_pairs = df_teacher.Timestamp_Pairs.to_list()
    
    return timestamp_pairs


def convert_time_to_seconds(timestamp):
    '''
    Convert timestamp to seconds (e.g. 01:22 --> 82)
    
    Inputs:
        - timestamp: timestamp in MM:SS format
        
    Returns:
        - timestamp in seconds    
    '''
    # Parse the timestamp as a datetime object
    time_obj = datetime.strptime(timestamp, '%M:%S')
    
    # Convert the datetime object to a timedelta object
    time_delta = timedelta(minutes=time_obj.minute, seconds=time_obj.second)
    
    # Convert the timedelta object to seconds
    return time_delta.total_seconds()


def create_timestamp_pairs(row, col, df):
    '''
    Create timestamp pair tuples using timestamp at current and next row
    
    Inputs:
        - row: index of current row
        - col: name of column with timestamp
        - df: dataframe
        
    Returns:
        - timestamp tuple (current row's timestamp, next row's timestamp)
    
    '''
    # Get the index of the current row
    index = row.name
    
    # Get the timestamp for the current row
    current_timestamp = row[col]

    # Check if there is a next row
    if index < len(df) - 1:
        # If there is, get the timestamp for the next row
        next_timestamp = df.loc[index + 1, col]
    else:
        # If there isn't, use the current timestamp value as a placeholder
        next_timestamp = current_timestamp

    # Create the tuple
    return (current_timestamp, next_timestamp)


def extract_teacher_audio(file_name, wav_path, teacher_wav_path, transcript_path, teacher_speaker_num):
    '''
    Extract the audio from the .wav file between each timestamp pair in the list.
    Saves as a new .wav file
    
    Inputs:
        - file_name: name of original file (without extension)
        - wav_path: directory containing .wav file
        - teacher_wav_path: directory to save .wav file with just teacher
        - transcript_path: directory containing transcript files
        - teacher_speaker_num: integer of which speaker number in the transcript corresponds to the teacher 
    
    Returns:
        - nothing, but saves teacher only audio to teacher_wav_path
    '''
    # Get timestamp pairs 
    # (list of pairs of timestamps (in seconds) in between which the teacher is speaking)
    timestamp_pairs = extract_teacher_timestamps(file_name, transcript_path, 2)
    
    
    with wave.open(wav_path + file_name + '.wav', 'rb') as wave_file:
        # Get the number of frames and the frame rate
        num_frames = wave_file.getnframes()
        frame_rate = wave_file.getframerate()

        # Initialize a list to hold the audio segments
        segments = []
        
        # If the teacher was the last to speak the last timestamp pair will have the wrong end time
        # Do a quick check and update if needed
        final_timestamp_pair = timestamp_pairs[-1]
        duration = num_frames / float(frame_rate)
        if final_timestamp_pair[0] == final_timestamp_pair[1]:
            timestamp_pairs[-1] = (final_timestamp_pair[0], duration) # Update to total duration of audio file
        
        # Iterate over the timestamp pairs and extract the corresponding audio segment
        for start, end in timestamp_pairs:
            start_frame = int(start * frame_rate)
            end_frame = int(end * frame_rate)
            wave_file.setpos(start_frame)
            segment_frames = wave_file.readframes(end_frame - start_frame)
            segment = np.frombuffer(segment_frames, dtype=np.int16)
            segments.append(segment)

    # Concatenate the audio segments
    concatenated_audio = np.concatenate(segments)

    # Create a new .wav file for the concatenated audio with just the teacher
    with wave.open(teacher_wav_path + file_name + '.wav', 'wb') as output_wave_file:
        output_wave_file.setnchannels(1)
        output_wave_file.setsampwidth(2)
        output_wave_file.setframerate(frame_rate)
        output_wave_file.setnframes(len(concatenated_audio))
        output_wave_file.writeframes(concatenated_audio.tobytes())
    


'''
Extract Features from Transcripts
'''

def extract_transcript_features(file_name, transcript_path, wav_path, teacher_speaker_num):
    '''
    Generate several features from transcript files (with timestamps and speaker labels) such as:
    
        - Duration including duration in seconds (total, teacher, and student), average duration (total, teacher, and student), and percent of the time that the teacher is the speaker.
        - Word count including total count (total, teacher, and student), percent of words said by teacher, and word rate (total, teacher, and student).
        - Line count (aka number of changes in speakers) including number of speaker changes (total line count) and number of time student/teacher speaks (student/teacher line count).
        
        
    Inputs:
        - file_name: name of original file (minus extension)
        - transcript_path: directory containing transcript files
        - wav_path: directory containing .wav file
        - teacher_speaker_num: integer of which speaker number in the transcript corresponds to the teacher 
    
    Returns:
        - dataframe with teacher ID and features
    '''
    # Read in transcript
    df = pd.read_csv(transcript_path + file_name + '.txt', 
                 engine = 'python', 
                 delimiter = "                                             ",
                 header = None)
    df.columns = ['Speaker', 'Timestamp', 'Text']
    
    # Create a column that converts the timestamps to seconds
    df['Timestamp_Secs'] = df['Timestamp'].apply(convert_time_to_seconds)
    
    # Create a column with pairs of timestamps
    df['Timestamp_Pairs'] = df.apply(create_timestamp_pairs, col = 'Timestamp_Secs', df = df, axis=1)
    
    # Create a column that is the duration (in seconds) of talking for each row
    df['Duration'] = df['Timestamp_Pairs'].apply(lambda x: x[1] - x[0])
    
    # Create a word count column
    df['Word_Count'] = df['Text'].str.split().str.len()
    
    # Update final timestamp's end time to total audio duration
    duration = get_total_duration(wav_path, file_name)
    df.iloc[-1]['Timestamp_Pairs'] = (df.iloc[-1]['Timestamp_Pairs'][0], duration)
    
    # Calculate speaking duration (for teacher vs students)
    df_teacher = df[df['Speaker'] == f'Speaker {teacher_speaker_num}:']
    df_student = df[df['Speaker'] != f'Speaker {teacher_speaker_num}:']
    teacher_duration = df_teacher.Duration.sum()
    student_duration = duration - teacher_duration
    
    # Count of lines (times spoken by teacher/students, number of speaker changes)
    total_lines = df.shape[0]
    teacher_lines = df_teacher.shape[0]
    student_lines = df_student.shape[0]
    
    # Word count calculations
    total_word_count = df.Word_Count.sum()
    teacher_word_count = df_teacher.Word_Count.sum()
    student_word_count = df_student.Word_Count.sum()
    
    # Create a dictionary with some features we may want from this data
    summary_dict = {'ID': file_name[0:3], 
                     # Duration realted features
                     'Total_Duration': duration,
                     'Teacher_Duration': teacher_duration,
                     'Student_Duration': student_duration,
                     'Percent_Time_Teacher': teacher_duration / duration,
                     'Average_Speaker_Duration': duration / total_lines,
                     'Average_Teacher_Duration': teacher_duration / teacher_lines,
                     'Average_Student_Duration': student_duration / student_lines,
                     # Word count features
                     'Total_Word_Count': total_word_count,
                     'Teacher_Word_Count': teacher_word_count,
                     'Student_Word_Count': student_word_count,
                     'Teacher_Percent_Words': teacher_word_count / total_word_count, 
                     'Total_Word_Rate': total_word_count / duration, 
                     'Teacher_Word_Rate': teacher_word_count / teacher_duration, 
                     'Student_Word_Rate': student_word_count / student_duration,
                     # Line count (times spoken, changes in speakers)
                     'Total_Speaker_Line_Count': total_lines,
                     'Teacher_Line_Count': teacher_lines,
                     'Student_Line_Count': student_lines,
                    }
    # Create dataframe with summary
    df_summary = pd.DataFrame(summary_dict, index = [0])
    
    return df, df_summary


def get_total_duration(wav_path, file_name):
    '''
    Calculate the total duration (in seconds) of the audio file
    
    Inputs:
        - wav_path: directory containing .wav file
        - file_name: name of original file (minus extension)
    
    Returns:
        - duration, in seconds
        
    '''
    with wave.open(wav_path + file_name + '.wav', 'rb') as wave_file:
        # Get the number of frames and the frame rate
        num_frames = wave_file.getnframes()
        frame_rate = wave_file.getframerate()

        # Calculate duration (in seconds)
        duration = num_frames / float(frame_rate)
        
    return duration


'''
Extract Audio/Speech Features 

using various python libraries to extract audio features

'''

def extract_audio_features(file_name, wav_path, num_mfccs = 13):
    '''
    Extract audio features using 3 libraries mentioned in this paper: https://www.jmir.org/2021/4/e24191/
    
    Inputs:
        - file_name: name of original file (minus extension)
        - wav_path: directory containing .wav file
        - num_mfccs: number of MFC coefficients to extract (default 13)
    
    Returns:
        - dataframe with teacher ID and summarized audio features
    '''
    
    # Features from My-Voice Analysis package
    df_my_voice = my_voice_analysis_features(file_name, wav_path)
    
    # Features from Python Speech Features library
    df_python_speech = python_speech_features(file_name, wav_path, num_mfccs = num_mfccs)
    
    # Features from Librosa library
    df_librosa = librosa_features(file_name, wav_path)
    
    # Create summary dataframe with ID from file name
    df_summary = pd.DataFrame({'ID': file_name[0:3]}, index = [0])
    
    # Combine into single dataframe
    df_summary = pd.concat([df_summary, df_my_voice, df_python_speech, df_librosa], axis=1)
    
    return df_summary
    
    
def my_voice_analysis_features(file_name, wav_path):
    '''
    Generate audio features such as balance, pauses, speaking rate, and f0 stats 
    from My-Voice-Analysis Library (https://github.com/Shahabks/my-voice-analysis)
    
    Inputs:
        - file_name: name of original file (minus extension)
        - wav_path: directory containing .wav file
    
    Returns:
        - dataframe with teacher ID and summarized audio features from my voice analysis package
    '''
    # Extract many summary metrics (e.g balance, pauses, speaking rate, f0 stats)
    df_summary = mysp.mysptotal(file_name, wav_path[:-1])
    
    # Extract "mood of speech"
    gender_mood = mysp.myspgend(file_name, wav_path[:-1])
    mood = extract_mood(gender_mood[0])
    df_summary['Mood'] = mood # Add mood to df
    
    return df_summary
    
    
def extract_mood(gender_mood_string):
    '''
    Extract the mood of speech from the gender and mood string from my-voice-analysis package's myspgend function
    
    For example, from the string:
    ('a female, mood of speech: Reading, p-value/sample size= :0.00', 5)
    I'd want to return "Reading"
        
    Inputs:
        - gender_mood_string: string output from my-voice-analysis package function
    
    Returns:
        - string just just the mood
    '''
    
    # Find the index of the first colon and the next comma after it
    colon_index = gender_mood_string.find(':')
    comma_index = gender_mood_string.find(',', colon_index)

    # Extract the text between the colon and comma using slicing
    mood = gender_mood_string[colon_index+2:comma_index]
    
    return mood
    
    
def python_speech_features(file_name, wav_path, num_mfccs = 13):
    '''
    Generate MFCC features using python speech features library (https://github.com/jameslyons/python_speech_features)
    
    For each of the mel-frequency cepstrum (MFC) coefficients calculate the mean, variance, skewness, and kurtosis for the energy (static coefficient), velocity (first differential), and acceleration (second differential).
    
    Inputs:
        - file_name: name of original file (minus extension)
        - wav_path: directory containing .wav file
        - num_mfccs: number of MFC coefficients to extract (default 13)
    
    Returns:
        - dataframe with teacher ID and summarized audio features
    '''
        
    # Extract info from audio file
    (rate, sig) = wav.read(wav_path + file_name + '.wav')
    
    # Extract MFCCs
    # can update num_mfccs if want to change the number of coefficients
    mfcc_feat = mfcc(sig, rate, nfft = 2000, numcep = num_mfccs)
    
    # Calculate aggregated metrics for each coefficient (mean, var, skew, etc.)
    df_mean = pd.DataFrame(mfcc_feat.mean(axis = 0)).T
    df_mean.columns = [f'MFCC_{i+1}_Mean' for i in range(num_mfccs)]
    df_var = pd.DataFrame(mfcc_feat.var(axis = 0)).T
    df_var.columns = [f'MFCC_{i+1}_Var' for i in range(num_mfccs)]
    df_skew = pd.DataFrame(skew(mfcc_feat)).T
    df_skew.columns = [f'MFCC_{i+1}_Skew' for i in range(num_mfccs)]
    df_kurtosis = pd.DataFrame(kurtosis(mfcc_feat)).T
    df_kurtosis.columns = [f'MFCC_{i+1}_Kurtosis' for i in range(num_mfccs)]
    
    # Combine into single dataframe
    df_mfcc = pd.concat([df_mean, df_var, df_skew, df_kurtosis], axis=1)

    return df_mfcc


def librosa_features(file_name, wav_path):
        '''
    Generate audio features using librosa library (https://pypi.org/project/librosa/)
    
    Calculate the mean, maximum, minimum, and standard deviation of the root mean square value, centroid, bandwidth, flatness, zero-crossing rate, and loudness of the spectrogram, or the visualization of the recording.
    
    Inputs:
        - file_name: name of original file (minus extension)
        - wav_path: directory containing .wav file
    
    Returns:
        - dataframe with teacher ID and summarized audio features
    '''
        
    # Load the WAV file using librosa
    y, sr = librosa.load(wav_path + file_name + '.wav')
    
    # Calculate statistics for different audio features from librosa library
    rms = pd.DataFrame(calc_mean_max_min_stdev(librosa.feature.rms(y=y))).T
    rms.columns = [f'RMS_{i}' for i in ['Mean', 'Min', 'Max', 'Std']]
    centroid = pd.DataFrame(calc_mean_max_min_stdev(librosa.feature.spectral_centroid(y=y))).T
    centroid.columns = [f'Centroid_{i}' for i in ['Mean', 'Min', 'Max', 'Std']]
    bandwidth = pd.DataFrame(calc_mean_max_min_stdev(librosa.feature.spectral_bandwidth(y=y))).T
    bandwidth.columns = [f'Bandwidth_{i}' for i in ['Mean', 'Min', 'Max', 'Std']]
    flatness = pd.DataFrame(calc_mean_max_min_stdev(librosa.feature.spectral_flatness(y=y))).T
    flatness.columns = [f'Flatness_{i}' for i in ['Mean', 'Min', 'Max', 'Std']]
    zero_crossing_rate = pd.DataFrame(calc_mean_max_min_stdev(librosa.feature.zero_crossing_rate(y=y))).T
    zero_crossing_rate.columns = [f'Zero_Crossing_Rate_{i}' for i in ['Mean', 'Min', 'Max', 'Std']]
    loudness = pd.DataFrame(calc_mean_max_min_stdev(librosa.amplitude_to_db(librosa.feature.rms(y=y)))).T
    loudness.columns = [f'Loudness_{i}' for i in ['Mean', 'Min', 'Max', 'Std']]

    # Combine into single dataframe
    df_librosa = pd.concat([rms, centroid, bandwidth, 
                            flatness, zero_crossing_rate, loudness], axis=1)

    return df_librosa

    
    
def calc_mean_max_min_stdev(array):
    '''
    Calculate mean, max, min, and standard deviation for an array
    
    Inputs:
        - array of numbers
        
    Returns:
        - list of mean, max, min, and standard deviation for that array
    '''
    return [np.mean(array), np.max(array), np.min(array), np.std(array)]
