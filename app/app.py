from ml_models.model_package_sklearn import model
from flask import Flask, request, jsonify, render_template

import numpy as np
import pandas as pd

import random
import time
import os

# initialize flask application
app = Flask(__name__)

# Fixing all seeds
def random_seed(seed_value):
    np.random.seed(seed_value)  # cpu vars
    random.seed(seed_value)  # Python


random_seed(500)


model_nb = model(r'ml_models', "nb_model.pkl")
model_svm = model(r'ml_models', "svm_model.pkl")
model_linreg = model(r'ml_models', "linreg_model.pkl")

# Define API
HOST = "0.0.0.0"
PORT = os.environ.get("PORT", 8080)

data = pd.read_csv(open("rawdata.csv", encoding='utf-8'))
cat = pd.read_csv(open("categories.csv", encoding='utf-8'))

cat_dict = cat.set_index('cat_id').to_dict()[' cat_name']


@app.route("/")
def index():
    return render_template("index.html", prediction={})


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
	For rendering results on HTML GUI
	"""
    if request.method == "POST":

        if request.form["submit_button"] == "Generate":
            i = random.sample(list(data.index), 1)[0]
            news_text = data["title"][i].replace(' - VnExpress', '')
            return render_template("index.html", prediction={}, news=str(news_text))

        elif request.form["submit_button"] == "Multinomial Naive Bayes":
            text_in = request.form["text"]
            if len(text_in) == 0:
                return render_template(
                    "index.html",
                    prediction={"ERROR": "Không có nội dung"},
                )
            else:
                # Check if text_in is in inference data
                filter1 = data["title"].isin([text_in])
                true_value = (
                    cat_dict[data["catidbase"][filter1].values[0]]
                    if filter1.any()
                    else ": Không tồn tại trong bộ dữ liệu"
                )
                output = model_nb.get_top_k(text_in, 3)
                return render_template(
                    "index.html",
                    prediction=output,
                    news=str(text_in),
                    real=str(true_value),
                )

        elif request.form["submit_button"] == "Support Vector Machine":
            text_in = request.form["text"]
            if len(text_in) == 0:
                return render_template(
                    "index.html",
                    prediction={"ERROR": "Không có nội dung"},
                )
            else:
                # Check if text_in is in inference data
                filter1 = data["title"].isin([text_in])
                true_value = (
                    cat_dict[data["catidbase"][filter1].values[0]]
                    if filter1.any()
                    else ": Không tồn tại trong bộ dữ liệu"
                )
                output = model_svm.get_top_k(text_in, 3)
                return render_template(
                    "index.html",
                    prediction=output,
                    news=str(text_in),
                    real=str(true_value),
                )

        elif request.form["submit_button"] == "Linear Regression":
            text_in = request.form["text"]
            if len(text_in) == 0:
                return render_template(
                    "index.html",
                    prediction={"ERROR": "Không có nội dung"},
                )
            else:
                filter1 = data["title"].isin([text_in])
                true_value = (
                    cat_dict[data["catidbase"][filter1].values[0]]
                    if filter1.any()
                    else ": Không tồn tại trong bộ dữ liệu"
                )
                output = model_linreg.get_top_k(text_in, 3)
                return render_template(
                    "index.html",
                    prediction=output,
                    news=str(text_in),
                    real=str(true_value),
                )

        elif request.form["submit_button"] == "Clear":
            return render_template("index.html", prediction={}, news="")

        else:
            pass

    elif request.method == "GET":
        return render_template("index.html", prediction={})


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
