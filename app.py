# coding: utf-8
from flask import Flask, render_template
from flaski.database import db_session
from flaski.models import ChartData
from datetime import datetime as dt

# appという名前でFlaskオブジェクトをインスタンス化
app = Flask(__name__)

@app.route('/')
def chart():
    # データベースからの値取得
    q = db_session.query(ChartData)
    chartdata = q.order_by(ChartData.id.asc()).limit(10)
    values1, values2, labels = [],[],[]
    for row in chartdata:
        values1.append(row.data1)
        values2.append(row.data2)
        labels.append(dt.strftime(row.date, '%Y-%m-%d-'))

    # 本来はJSONにパースして渡してあげなければいけない？
    return render_template('chart.html', values1=values1, values2=values2, labels=labels)

# -- Main関数 --
if __name__ == '__main__':
    app.run(debug=True)

# 動画50分から再開
