import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import TfidfModel
from gensim.matutils import corpus2dense
from scipy.spatial.distance import pdist, squareform

def performer_model(text_data):
    tfidf = TfidfModel(text_data)
    dense = corpus2dense(tfidf[text_data], num_words=len(tfidf.wv.vocab)).T
    similarity_matrix = cosine_similarity(dense)
    return similarity_matrix