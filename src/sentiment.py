from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def score_sentiment(text):
    if isinstance(text, str):
        score = analyzer.polarity_scores(text)['compound']
        return score
    else:
        return None
