import pandas as pd
import datetime
df = pd.read_csv('fb_posts_data.csv')

from pymongo import MongoClient
import json
db = MongoClient().fb

db.fb_posts.drop()
data = json.loads(df.T.to_json())

db.fb_posts.insert(df.to_dict('records'))
