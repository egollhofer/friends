import pandas as pd

# Packages needed for emotionality estimation
from gensim.models import Word2Vec
import nltk

# Packages needed for intimacy estimation
import re
from question_intimacy.predict_intimacy import IntimacyEstimator
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from torch import Tensor
import numpy as np
import math

# Packages needed for sentiment estimation
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Import other methods from src
import intimacy
import sentiment
import emotionality

characterlist = ["Chandler Bing", "Joey Tribbiani", 'Monica Geller', "Phoebe Buffay", "Rachel Green", "Ross Geller"]

if __name__ == '__main__':
    dialog_df = pd.read_csv("data/friends.csv")
    dialog_df['sentiment_score'] = dialog_df['text'].apply(sentiment.score_sentiment)
    print('sentiment done')
    dialog_df['question'] = dialog_df['text'].apply(intimacy.find_questions)
    dialog_df['intimacy_score'] = dialog_df['question'].apply(intimacy.score_intimacy)
    print('intimacy done')
    dialog_df = emotionality.emotionality_main(dialog_df)
    print('emo done')
    dialog_df.to_csv("data/friends_scored.csv", index=False)
