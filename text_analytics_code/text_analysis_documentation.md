# Text Analysis Documentation 
 
This file goes over the different methods and analysis applied to the transcribed transcripts of the IDEA mindfulness study. 

### Relevant File Schemas

A list and description of the files used in the analysis

##### TOKEN.csv: A hierarchical file that represents each token (word) as a single row

|Field |Description|
|----- |-----------|
|speaker_id|unique id of teacher|
|line_num  |position of the 'paragraph' within the text|
|sent_num  |position of the sentence within a line|
|token_num |position of the token within a sentence|
|pos_tuple |tuple in the format ('token_str', 'pos')|
|pos       |the token's part of speech|
|token_str |the token (word) as it appears in text|
|term_str  |the token after removing punctuation and capitilization|
|term_id   |unique_id of the term|

##### LIB.csv: Library file that contains source information

|Field |Description|
|----- |-----------|
|speaker_id|unique id of teacher|
|book_file |filename of the transcribed transcript|

##### DOC.csv: A hierarchical file that represents each line as a single row

|Field |Description|
|----- |-----------|
|speaker_id|unique id of teacher|
|line_num  |position of the 'paragraph' within the text|
|line_str  |the text of the line as a string|

##### TFIDF.csv: 

## Sentiment Analysis

This is a technique where we analyzed each piece of text to determine the sentiment behind it. The analysis focuses on emotion detection also known as a lexicon method of sentiment analysis. Sentiments such as happy, sad, anger, and so on come under emotion detection. 

See [sentiment_analysis.ipynb](https://github.com/eycooper/capstone/tree/main/text_analytics_code/sentiment_analysis.ipynb) for code


### Lexicon

The lexicon used in this analysis is [NRC.csv](https://github.com/eycooper/capstone/blob/main/text_analytics_code/NRC.csv) which was downloaded from [kaggle](https://www.kaggle.com/datasets/andradaolteanu/bing-nrc-afinn-lexicons). This lexicon includes 8 different emotions as well as polarity variables as sentiments. Each row contains a word and a sentiment that word induces. 

|word|sentiment|
|----|---------|
|abandon|fear|
|abandon|negative|
|abandon|sadness|

To conduct the analysis we transform the file, the sentiment values become column headers and take binary values, 0 if the word doesn't induce the sentiment and 1 if it does.

|word|anger|anticipation|disgust|fear|joy|negative|positive|sadness|surprise|trust|
|---|---|---|---|---|---|---|---|---|---|---|
|abandon|0|0|0|1|0|1|0|1|0|0|

The lexicon is then joined with TOKEN.csv. 

### Visuals

Description of visuals created in the Sentiment Analysis file.

## Sentiment Bar Charts

![Sentiment Bar Charts](/sentiment_bar_charts/201.png)

These bar charts are a visual representation of the average sentiment present in the document/body of text given. The numerical values are calculated by summing up each instance of a word that induces that emotion and then divided by the number of tokens present. 

### Vader Metrics

![positive_negative](/pos_neg/speaker_201.png)
![neutral](/neu/speaker_201.png)
![compound](/compound/speaker_201.png)

Using the VaderSentiment library, three line graphs are generated. The pos, neu, and neg scores are ratios for proportions of text that fall in each category (so these should all add up to be 1 or close to it with float operation). The compound score is computed by summing the valence scores of each word in the lexicon, adjusted according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive). This is the most useful metric if you want a single unidimensional measure of sentiment for a given sentence. Calling it a ‘normalized, weighted composite score’ is accurate.

