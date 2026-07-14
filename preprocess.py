import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required resources automatically
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

stop_words = set(stopwords.words("english"))


def preprocess_text(text):
    """
    Clean and preprocess user text.
    """

    text = text.lower()

    tokens = word_tokenize(text)

    tokens = [
        word for word in tokens
        if word not in string.punctuation
    ]

    tokens = [
        word for word in tokens
        if word not in stop_words
    ]

    return " ".join(tokens)