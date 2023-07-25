import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MOVIE_DICT = pickle.load(open("movie_dict.pkl", "rb"))
MOVIES = pd.DataFrame(MOVIE_DICT)

cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(MOVIES['tags']).toarray()
SIMILARITY = cosine_similarity(vectors)