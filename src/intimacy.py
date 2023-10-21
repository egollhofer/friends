import re
from question_intimacy.predict_intimacy import IntimacyEstimator
inti = IntimacyEstimator()


def find_questions(text):
    """
    Takes dialog utterance as input, and returns a question
    Args:
        text: Utterance of dialog as a string
    Returns:
        If there is a question of more than 4 words, it is returned.
        Else returns None
    """
    pattern = r'\b[A-Za-z\s,\']*\?'
    if isinstance(text, str):
        qs = re.findall(pattern, text)
        for q in qs:
            if len(q.split()) >= 4:
                return q
    return ""


def score_intimacy(question):
    """
    Takes question as input, returns intimacy score of the question
    Args:
        question: either string question, or None
    Returns:
        If question is "" returns None
        Otherwise, returns the intimacy score of the question
    """
    if question is not None:
        return inti.predict(question)
    else:
        return None
