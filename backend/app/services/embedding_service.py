from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_embedding(text):
    return text  # raw text

def compute_similarity(cv_text, job_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([cv_text, job_text])
    return cosine_similarity(vectors[0], vectors[1])[0][0]