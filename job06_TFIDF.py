import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

df_reviews  = pd.read_csv('./crawling_data/cleaned_one_review.csv')
df_reviews.info()

#Tfidf 값을 저장한다.
#TF 한단어가 한문장에서 그 문장에서 등장한 횟수
#단어가 전체 문장에서 단어가 들어간 문자의 개수의 역수
Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['reviews'])
print(Tfidf_matrix.shape)

with open('./models/tfidf.pickle','wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/Tfidf_movie_review.mtx', Tfidf_matrix)