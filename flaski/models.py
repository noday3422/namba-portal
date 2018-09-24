# coding: utf-8
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from flaski.database import Base
from datetime import datetime as dt

#Table情報
class ChartData(Base):
    #TableNameの設定
    __tablename__ = "chartdata"
    #Column情報を設定する
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, unique=False)
    data1 = Column(Integer, unique=False)
    data2 = Column(Integer, unique=False)
    timestamp = Column(DateTime, default=dt.now())

    def __init__(self, date=None, data1=None, data2=None, timestamp=None):
        self.date = date
        self.data1 = data1
        self.data2 = data2
        self.timestamp = timestamp
