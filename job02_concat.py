import pandas as pd
import re



df = pd.read_csv('./crawling_data/merged_reviews.csv')
X = df['review']
print(X.head())
for i in range(len(X)):
     X[i] = re.compile('[^가-힣]').sub(' ',str(X[i]))
df['review']=X
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df.to_csv('./final_review.csv',index=False)