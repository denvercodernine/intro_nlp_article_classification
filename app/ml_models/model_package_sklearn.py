import pickle
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

cat_ids = {1001005: "Thời sự", 1001002: "Thế giới", 1003159: "Kinh doanh", 1002691: "Giải trí", 1002565: "Thể thao",
           1001007: "Pháp luật", 1003497: "Giáo dục", 1003750: "Sức khỏe", 1002966: "Đời sống", 1003231: "Du lịch", 1001009: "Khoa học"}


class model():
    def __init__(self, ModelPath, ModelName):
        self.count_vectorizer = CountVectorizer(vocabulary=pickle.load(
            open(os.path.join(os.getcwd(), ModelPath, "count_vector.pkl"), "rb")))
        self.tfidf = pickle.load(
            open(os.path.join(os.getcwd(), ModelPath, "tfidf.pkl"), "rb"))
        self.model = pickle.load(
            open(os.path.join(os.getcwd(), ModelPath, ModelName), "rb"))

    def get_top_k(self, text, k):
        text = [text]

        X_new_counts = self.count_vectorizer.transform(text)
        X_new_tfidf = self.tfidf.transform(X_new_counts)
        predictions = self.model.predict_proba(X_new_tfidf)

        best_k = np.argsort(predictions, axis=1)[:, -k:]

        # dictionnary of predicted classes with their probabilities
        results = {
            cat_ids[self.model.classes_[i]]: "{:12.2f}%".format(
                float(predictions[0][i]) * 100)
            for i in best_k[0][::-1]
        }
        return results


if __name__ == "__main__":
    name = input("Enter model name (with exstension):")
    text = input("Enter text to be predicted:")
    Model = model(r'model', name)
    print(Model.get_top_k(text, 3))
