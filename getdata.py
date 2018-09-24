import urllib
from bs4 import BeautifulSoup
import datetime

# return:日付・最高気温・最低気温・平均気温
def getData():

    # 戻り値（グローバルで宣言したかったけど、うまく動かないから妥協）
    dateValues, aveValues, maxValues, minValues = [], [], [], []

    # 現在の日付からURLを生成してデータ取得関数に投げる
    urlFormat = 'https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year={}&month={}&day=&view='
    # 今月
    year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    url = urlFormat.format(year, month)
    # 先月
    ｍonth2 = month - 1
    year2 = year
    if month2 == 0:
        month2 = 12
        year2 -= 1
    url2 = urlFormat.format(year2, month2)

    # それぞれデータ取得（先月→今月）
    getMonthData(url2, year2, month2, dateValues, aveValues, maxValues, minValues)
    getMonthData(url, year, month, dateValues, aveValues, maxValues, minValues)

    return dateValues, aveValues, maxValues, minValues


def getMonthData(url, year, month, dateValues, aveValues, maxValues, minValues):

    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    all = soup.find_all('tr', class_='mtx')
    AVE = 5 # 平均気温が5番目
    MAX = 6 # 最高気温が6番目
    MIN = 7 # 最低気温が7番目

    for i in range(len(all)):
        if i < 4:
            # 最初の4行はヘッダ
            continue
        row = all[i].find_all('td', class_='data_0_0')
        if row[AVE].text != '':
            dateValues.append('{}年{}月{}日'.format(year, month, i-3))
            aveValues.append(row[AVE].text)
            maxValues.append(row[MAX].text)
            minValues.append(row[MIN].text)
