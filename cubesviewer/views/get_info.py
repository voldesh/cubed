from pymongo import MongoClient
from datetime import datetime, timedelta, date

def get_all_data():
	mc = MongoClient()
        db = mc.olap

	data = []

	today = str(date.today())

        today_minus7 = str(date.today() - timedelta(days=7))

        #get only week old ids
	for i in db.post_history.find({"insights": { "$elemMatch" : { "date": {"$gte": today_minus7, "$lt": today}}}}):
		ctime = i["created_time"][:10]
		data.append([i["_id"], ctime])

	return data

def get_all_authors():
	mc = MongoClient()
        db = mc.olap

        data = []

        today = str(date.today())

        today_minus7 = str(date.today() - timedelta(days=7))

        #get only week old ids
        for i in db.post_history.find({"insights": { "$elemMatch" : { "date": {"$gte": today_minus7, "$lt": today}}}}):
                if i['author'] not in data:
	                data.append(i['author'])

        return data

