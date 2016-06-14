from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
import sys
import logging

def load_data(file_name):
    csv_data = []
    with open(file_name, 'rb') as f:
        data = csv.reader(f)
        for d in data:
            csv_data.append(d)

    return csv_data

Base = declarative_base()


class FB_Data(Base):
    # Tell SQLAlchemy what the table name is and if there's any table-specific
    # arguments it should know about
    __tablename__ = 'FB_POSTS_DATA'

    # tell SQLAlchemy the name of column and its attributes:
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String(100))
    message = Column(String(100))
    category = Column(String(100))
    like = Column(Integer)
    share = Column(Integer)
    comment = Column(Integer)
    ctr = Column(Float)


class Key_Data(Base):
    __tablename__ = 'KEYWORDS_DATA'

    # tell SQLAlchemy the name of column and its attributes:
    id = Column(String(100))
    keywords = Column(String(100), primary_key=True)
    like = Column(Integer)
    share = Column(Integer)
    comment = Column(Integer)
    ctr = Column(Float)

if __name__ == "__main__":
    t = time()

    logging.basicConfig(filename='api.log', level=logging.DEBUG)

    # Create the database
    engine = create_engine('sqlite:///myData.sqlite')
    #engine.raw_connection().connection.text_factory = str

    Base.metadata.create_all(engine)

    # Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    ids = []

    for dt in s.query(FB_Data):
        ids.append(str(dt.id))

    file_name1 = "fb_posts_data.csv"
    file_name2 = "keywords_data.csv"

    fb_data = load_data(file_name1)
    key_data = load_data(file_name2)

    for i in range(len(fb_data)):
        if i > 0:
            if fb_data[i][0] not in ids:
                ids.append(fb_data[i][0])
            else:
                dat1 = s.query(FB_Data).filter_by(id=fb_data[i][0]).first()
                s.delete(dat1)

            fb_record = FB_Data(**{
                'id': fb_data[i][0],
                'name': fb_data[i][1],
                'message': fb_data[i][2],
                'category': fb_data[i][3],
                'like': fb_data[i][4],
                'share': fb_data[i][5],
                'comment': fb_data[i][6],
                'ctr': fb_data[i][7]
            })
            s.add(fb_record)

    keys = []

    for dt in s.query(Key_Data):
        keys.append(str(dt.keywords))

    for i in range(len(key_data)):
        if i > 0:
            if key_data[i][1] not in keys:
                keys.append(key_data[i][1])
            else:
                dat2 = s.query(Key_Data).filter_by(
                    keywords=key_data[i][1]).first()
                s.delete(dat2)

            key_record = Key_Data(**{
                'id': key_data[i][0],
                'keywords': key_data[i][1],
                'like': key_data[i][2],
                'share': key_data[i][3],
                'comment': key_data[i][4],
                'ctr': key_data[i][5]
            })

            s.add(key_record)

    s.commit()  # Attempt to commit all the records

    s.close()  # Close the connection

    logging.debug("Time elapsed: " + str(time() - t) + " s.")
