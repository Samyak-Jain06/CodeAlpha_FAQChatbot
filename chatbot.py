import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import preprocess_text


class FAQChatbot:

    def __init__(self, faq_file="faq.csv"):

        self.data = pd.read_csv(
    faq_file,
    quotechar='"',
    skipinitialspace=True,
    encoding="utf-8"
    )

        self.questions = self.data["Question"].tolist()
        self.answers = self.data["Answer"].tolist()

        self.cleaned_questions = [
            preprocess_text(question)
            for question in self.questions
        ]

        self.vectorizer = TfidfVectorizer()

        self.question_vectors = self.vectorizer.fit_transform(
            self.cleaned_questions
        )

    def get_response(self, user_question):

        cleaned_question = preprocess_text(user_question)

        user_vector = self.vectorizer.transform([cleaned_question])

        similarity = cosine_similarity(
            user_vector,
            self.question_vectors
        )

        best_match = similarity.argmax()

        confidence = similarity[0][best_match]

        if confidence < 0.25:
            return (
            "❓ I couldn't find an answer to that.\n\n"
            "Try asking about:\n"
            "• Python\n"
            "• Artificial Intelligence\n"
            "• GitHub\n"
            "• Windows\n"
            "• RAM\n"
            "• SSD\n"
            "• Networking",
            confidence
            )

        return (
            self.answers[best_match],
            confidence
        )