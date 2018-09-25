# coding: utf-8
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flaski.database import db_session
from flaski.models import ChartData
from datetime import datetime as dt
import getdata as gd
import json
import pandas as pd
import requests
import os
from werkzeug import secure_filename
from PIL import Image
import numpy as np
import chainer
import chainer.links as L
import chainer.functions as F
from model import CNN

# appという名前でFlaskオブジェクトをインスタンス化
app = Flask(__name__)

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg'])

# modelの読み込み
model_cnn = L.Classifier(CNN())
chainer.serializers.load_npz('dog_cat.npz', model_cnn)

# 犬猫ラベル
labels = {
    '0':'犬',
    '1':'猫'
}

# グローバル関数（と言いつつ、使うのは犬猫予測だけなので、本当はファイル分けたい。

# 犬猫推論実行(Numpy形式で画像が入ってくる前提)
def infer(x):
    x = x[np.newaxis]
    y = model_cnn.predictor(x)
    y = F.softmax(y).data
    y = np.argmax(y, axis=1)
    # ここってToStringしてるだけ？イケてなくない？
    label = '{}'.format(y[0])
    return labels[label]

# ファイルの拡張子チェック
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# -- View側の設定　--
# rootディレクトリにアクセスした場合の挙動
# def以下がアクセス後の挙動
@app.route('/')
def index():
    #return 'Hello World!'
    # DBから以下の変数を読み込んできたと仮定
    title = 'NambaPortal'
    message = 'MTVデザインパターンでWebアプリ作成　'
    return render_template('index.html', title=title, message=message)

# -- 家賃予測 --
@app.route('/predict-house')
def predictHouse():
    return render_template('predict-house.html')

@app.route('/predict-house-result', methods=['POST'])
def predictHouseResult():

    index = request.form['index']
    url = 'https://predict-house.herokuapp.com'
    df = pd.read_csv('static/PredictModel/housing.csv')
    x_post = {'x_post':str(list(df.iloc[int(index),:-1].values))}
    res = requests.post(url, json=x_post)
    result = float(res.json()['y'])
    price = result * 1000
    # まずはダミーのデータでWebAPIを叩き、結果を画面に表示するところまで
    return render_template('predict-house-result.html', result=result, price=price)

@app.route('/chart')
def chart():
    # データベースからの値取得
    q = db_session.query(ChartData)
    chartdata = q.order_by(ChartData.id.asc()).limit(10)
    values1, values2, labels = [],[],[]
    for row in chartdata:
        values1.append(row.data1)
        values2.append(row.data2)
        labels.append(dt.strftime(row.date, '%Y-%m-%d-'))
    return render_template('chart.html', values1=values1, values2=values2, labels=labels)

@app.route('/temperature')
def temperature():
    # 今月・先月の東京の気温を取得
    # JSに渡してグラフ表示
    dateValues, aveValues, maxValues, minValues = gd.getData()
    #dateValues, aveValues, maxValues, minValues = getData()
    return render_template('temperature.html', dateValues=dateValues, aveValues=aveValues, maxValues=maxValues, minValues=minValues)

@app.route('/dog_cat', methods=['GET', 'POST'])
def dogCat():
    if request.method == 'POST':
        # dog_cat.htmlにてPOST要求が発生したらdisplay_img.htmlに渡す
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
        return render_template('display_img.html', file_path=file_path)
    else:
        # GETの場合はdog_cat.htmlを返す
        return render_template('dog_cat.html')

@app.route('/classify', methods=['GET', 'POST'])
def classify_img():
    if request.method=='POST':
        file_path = request.form['image']
        img = Image.open(file_path)
        img = img.resize((224,224))
        x = np.array(img, 'f').transpose(2,0,1)
        label = infer(x)
        #label = '犬'
        # inferが遅いことは確認済み。
        # localで動かすと数秒で返ってくる処理がheroku上だとタイムアウトする。なぜか。

        return render_template('classify_img.html', label=label, file_path=file_path)

# -- Main関数 --
if __name__ == '__main__':
    app.run(debug=True)
