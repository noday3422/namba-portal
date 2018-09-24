# coding: utf-8
from flask import Flask, render_template, jsonify, request
from flaski.database import db_session
from flaski.models import ChartData
from datetime import datetime as dt
import getdata as gd
import json
import pandas as pd
import requests

# appという名前でFlaskオブジェクトをインスタンス化
app = Flask(__name__)

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

# -- Main関数 --
if __name__ == '__main__':
    app.run(debug=True)
