import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from PyQt5.QtCore import QStringListModel
form_window  = uic.loadUiType('./movie_recommendation.ui')[0]


class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
        with open('./models/tfidf.pickle','rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
        self.df_reviews = pd.read_csv('./crawling_data/cleaned_one_review.csv')
        self.titles = list(self.df_reviews['titles'])
        self.titles.sort()
        for title in self.titles:
            self.comboBox.addItem(title)

        model = QStringListModel()
        model.setStringList(self.titles)
        completer = QCompleter(model)
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)

        self.comboBox.currentIndexChanged.connect(self.combobox_slot)
        self.btn_recommendation.clicked.connect(self.btn_slot)

    def btn_slot(self):
        keyword = self.le_keyword.text()
        self.le_keyword.setText('')
        if keyword:
            if keyword in self.titles:
                recommendation = self.recommendation_by_movie_title(keyword)
                self.lbl_recommendation.setText(recommendation)
            else :
                recommendation = self.recommendation_by_keyword(keyword)
                self.lbl_recommendation.setText(recommendation)

    def recommendation_by_keyword(self,keyword):
        try:
            sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
            print(sim_word)
            words = [keyword]
            for word, _ in sim_word:
                words.append(word)
            print(words)

            # 가장 많이 나온 단어는 10개 그 다음은 9개 그 다음은 8개 ...
            sentence = []
            count = 10
            for word in words:
                sentence = sentence + [word] * count
                count-=1
            sentence = ' '.join(sentence)
            print(sentence)
            sentence_vec = self.Tfidf.transform([sentence])
            cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
            recommendation = self.getRecommendation(cosine_sim)
            print(recommendation)
            return recommendation
        except:
           return '다른 키워드를 이용하세요.'
    def getRecommendation(self,cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        movieIdx = [i[0] for i in simScore]
        recMovieList = self.df_reviews.iloc[movieIdx, 0]
        print(recMovieList)
        recMovieList = '\n'.join(recMovieList[1:])

        return recMovieList

    def combobox_slot(self):
        title = self.comboBox.currentText()
        recommendation=self.recommendation_by_movie_title(title)
        self.lbl_recommendation.setText(recommendation)
    def recommendation_by_movie_title(self,title):
        movie_idx = self.df_reviews[self.df_reviews['titles']==title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        return recommendation

if __name__=='__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())