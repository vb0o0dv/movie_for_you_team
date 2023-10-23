import pandas as pd
import glob
import datetime

data_path = glob.glob('./crawling_data/review_*')
print(data_path)

df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path)
    df = pd.concat(([df, df_temp]))

print(df.head())
print(df['title'].value_counts())
df.info()
df.to_csv('./crawling_data/review_201910_202109.csv',index=False)