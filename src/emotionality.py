from gensim.models import Word2Vec
import nltk
import re
from nltk import SnowballStemmer
import joblib
import numpy as np
from scipy.spatial.distance import cosine

snow_stemmer = SnowballStemmer(language='english')
global model
global centroid_size
global freqs
global cognition_centroid
global affect_centroid

characterlist = ["Chandler Bing", "Joey Tribbiani", 'Monica Geller', "Phoebe Buffay", "Rachel Green", "Ross Geller"]

STOPS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
         'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
         'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
         'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
         'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
         'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
         'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
         'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
         'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
         'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
         'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
         'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 've', 'll', 'amp']

def preprocess_emotionality(text):
    """
    Takes dialog utterance as input, and returns the text preprocessed according to Gennaro et al
    Args:
        text: Utterance of dialog as a string
    Returns:
        text, processed according to Gennaro et al:
            All words lowercased, numbers and punctuation removed, stopwords removed, short words removed, stemmed
    """
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'[^\sA-Za-z0-9À-ÖØ-öø-ÿЀ-ӿ/]', ' ', text)
        text = ' '.join([word for word in text.split() if word not in STOPS])
        text = ' '.join([word for word in text.split() if not len(word) < 2])
        text = ' '.join([snow_stemmer.stem(word) for word in text.split()])
        return text
    else:
        return ''


def get_corpus_vocab(corpus_df):
    """
    Takes dialog dataframe as an argument, returns a list of the vocabulary and a count for each token
    Args:
        corpus_df: DataFrame of dialog corpus
    Returns:
        test_list: A list of words in the corpus
        freqs: A dictionary mapping words to their count in the corpus
    """
    text_list = []
    freqs = {}
    for text in corpus_df['text_processed']:
        if isinstance(text, str):
            tokens = nltk.word_tokenize(text)
            for token in tokens:
                if token in freqs:
                    freqs[token] += 1
                else:
                    freqs[token] = 1
            text_list.append(tokens)
    return text_list, freqs


def train_model(text_list):
    """
    Takes vocabulary list as input, returns a trained Word2Vec model
    Args:
        text_list: list of vocabulary items (strings)
    Returns:
        w2v_model: Trained Word2Vec model, with parameters set according to Gennaro et al
    """
    w2v_model = Word2Vec()
    w2v_model.build_vocab(text_list)
    w2v_model.train(text_list, total_examples=w2v_model.corpus_count, epochs=w2v_model.epochs)
    return w2v_model

def find_centroid(text, model, freqs):
    """
    Takes list of words, trained Word2Vec model, and frequency count as input, and returns a vector representation
    of the words
    Args:
        text: list of words (strings)
        model: trained Word2Vec model
        freqs: dictionary count mapping words to their count in the corpus
    Returns:
        centroid: an average vector representation of the words in the text
    """
    vecs = [model.wv[w] * freqs[w] for w in text if w in model.wv]
    vecs = [v for v in vecs if len(v) > 0]
    centroid = np.mean(vecs, axis=0)
    centroid = centroid.reshape(1, -1)
    return centroid

def add_centroid(text):
    """
    Takes dialog utterance and returns a vector representation of the utterance
    Args:
        text: string dialog utterance
    Returns:
        centroid: an average vector representation of the words in the text
    """
    global model
    global freqs
    global centroid_size
    if isinstance(text, str):
        split_text = text.split()
        centroid = find_centroid(split_text, model, freqs)
        if centroid.size == centroid_size:
            return centroid
    return None

def calculate_emotionality_score(v):
    """
    Takes vector and returns an average emotionality score
    Args:
        v: numpy vector representation of a dialog utterance
    Returns:
        score: a float representing the emotionality of the utterance.  Larger values are closer to the affect vector
    """
    global cognition_centroid
    global affect_centroid
    if v is not None:
        v = v.reshape(1, -1)
        v = v.tolist()
        emo_list = affect_centroid.tolist()
        cog_list = cognition_centroid.tolist()
        a = cosine(v[0], emo_list[0])
        c = cosine(v[0], cog_list[0])
        score = (1 + 1 - a)/(1 + 1 - c)
        return score
    return None

def emotionality_main(df):
    global model
    global freqs
    global centroid_size
    global cognition_centroid
    global affect_centroid
    # First process the text per research paper
    df['text_processed'] = df['text'].apply(preprocess_emotionality)
    # get the vocabulary, frequency of tokens, and train Word2Vec model on this corpus
    text_list, freqs = get_corpus_vocab(df)
    model = train_model(text_list)
    # load a list of words representing our two poles - cognition and affect
    cognition = joblib.load("data/dictionary_cognition.pkl")
    affect = joblib.load("data/dictionary_affect.pkl")
    cognition_centroid = find_centroid(cognition, model, freqs)
    affect_centroid = find_centroid(affect, model, freqs)
    centroid_size = cognition_centroid.size
    df['centroid'] = df['text_processed'].apply(add_centroid)
    df['emotionality_score'] = df['centroid'].apply(calculate_emotionality_score)
    return df
    # at this point, I have a centroid for each utterance
    # Next, I need to separate things out by character so I can get the average emotionality for a conversation
    # First make subsets of the speaker, and then sub-subsets with the reply_to
    # Then for each conversation ID, find the average distance of all vectors


