import pandas as pd
from konlpy.tag import Okt
import re
from tqdm import tqdm
df = pd.read_csv('./crawling_data/merge_reviews_professor.csv')
df.info()

okt = Okt()

df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])
use_class = ['Noun','Verb','Adjective']
cleaned_sentences = []
for review in tqdm(df.review):
    review = re.sub('[^가-힣]',' ',review)
    tokened_review = okt.pos(review, stem=True)
    #print(tokened_review)

    df_token = pd.DataFrame(tokened_review, columns=['word','class'])
    df_token = df_token[(df_token['class']=='Noun')|
                        (df_token['class']=='Verb')|
                        (df_token['class']=='Adjective')
    ]
    #print(df_token.head())
    words = []
    for word in df_token.word:
        if len(word)>1:
            if not word in stopwords:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df['cleaned_sentences'] = cleaned_sentences
df = df[['title','cleaned_sentences']]
print(df.head(10))
df.info()
df.to_csv('./crawling_data/cleaned_review.csv', index=False)