# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.db') #dbファイル名と保存先を指定する（同ディレクトリにdata.dbというファイルを作成）
engine = create_engine('sqlite:///' + databese_file, convert_unicode=True , echo=True) #sqliteを指定
db_session = scoped_session(
                sessionmaker(
                    autocommit = False,
                    autoflush = False,
                    bind = engine
                )
             )
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import flaski.models
    Base.metadata.create_all(bind=engine)
