# Text Analysis Documentation 
 
This file goes over the different methods and analysis applied to the transcribed transcripts of the IDEA mindfulness study. 

### Relevant Files

A list and description of the files used in the analysis

* TOKEN.csv: A hierarchical file that represents each word (token) as a single row
    ** speaker_id - unique id of the teacher/speaker
    ** line_num - the number of the line the word appears in
    ** sent_num - the number of the sentence the word appears in (note that the sentence count is within the line, so a new line starts the count over)
    ** token_num - the number of the word within each sentence
    ** pos_tuple - 
    ** pos - 
    ** token_str - 
    ** term_str - 
    ** term_id - 

## Sentiment Analysis

This is a technique where we analyzed each piece of text to determine the sentiment behind it. The analysis focuses on emotion detection also known as a lexicon method of sentiment analysis. Sentiments such as happy, sad, anger, and so on come under emotion detection. 

See [sentiment_analysis.ipynb](https://github.com/eycooper/capstone/tree/main/text_analytics_code/sentiment_analysis.ipynb)



