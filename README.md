# The Problem Statement
## Goal 
Given a code-mixed dataset, corresponding languages should be identified

## Methods/Variants
Hidden Markov Models(HMM's),Conditional Random Fields(CRF's), Maximum Entropy Markov Models(MEMM's)

## Baselines:
* Find lexical classification into the known set of languages.
* Finding the base grammatical structure of the code-mixed data.

## Take it forward:
* Word Level classification experiments can be carried out using a simple dictionary-based method, linear kernel support vector machines (SVMs) with and without contextual clues, and a k-nearest neighbour approach(http://grzegorz.chrupala.me/papers/EMNLP_Workshop_CodeMixing__Final.pdf)
* Embedding Matrix of individual languages can be used to evaluate the grammaticality of the code-mixed data

# Solution Space
## Data
The data being chosen for this project is the data used in the paper "A Corpus of English-Hindi Code-Mixed Tweets
for Sarcasm Detection" (Swami et. al., 2018) (https://github.com/sahilswami96/SarcasmDetection_CodeMixed/blob/master/Dataset/Sarcasm_tweets_with_language.txt).

## Task definition
We treat the task of language identification as a sequence labelling problem, in which each word is going to be assigned the tag of the language as provided in the training data. The training data chosen here uses only 'en' and 'hi' labels for English and Hindi (and 'rest' for other words which are ambiguous or punctuation and other common words and symbols in both languages), but hopefully this can be extended to code-mixed datasets and languages. 

## Current Approaches
Language identification of codemixed data was a Workshop Task to COLING 2014. Some of the approaches that exist for this task include dictionary based methods, support vector machines and conditional random fields. We have attempted these methods on our data.

## Our Approach
Sub-word level LSTMs have been used for sentiment analysis of code mixed data. A combination of a subword LSTM and a CRF for the sequence labelling is the first of our approaches. The second is an attempt to capture syntax as well, so a CNN with a subword Bi-LSTM and a CRF for the sequence labelling will be the two approaches to be used. 