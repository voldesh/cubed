from datetime import datetime, timedelta
import sys
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.http import JsonResponse

#------------------------------------------------------------#

def get_post_by_shares(mid):
	mc = MongoClient()
        
        db = mc.olap

        shares = {}
       	shares['_id'] = mid
        shares['insights'] = []

        rec = db.post_history.find({"_id":ObjectId(mid)})

	if rec.count() != 1:
		return JsonResponse(json.dumps({"error": "invalid id"}), safe=False)

        for r in rec:
                sha = r

        for ins in sha['insights']:
                shared = ins['share']

                shared_dict = {}
                shared_dict['engagements'] = shared

                shares['insights'].append(shared_dict)
	
    	return JsonResponse(json.dumps(shares), safe=False)


#------------------------------------------------------------#

def get_post_by_engagements(mid):
	mc = MongoClient()	
	
	db = mc.olap

        engagements = {}
	engagements['_id'] = mid
	engagements['insights'] = []
	
	rec = db.post_history.find({"_id":ObjectId(mid)})

	if rec.count() != 1:
                return JsonResponse(json.dumps({"error": "invalid id"}), safe=False)

	for r in rec:
		eng = r

	for ins in eng['insights']:
		engaged = ins['comment'] + ins['share'] + ins['like']

		engaged_dict = {}
		engaged_dict['engagements'] = engaged

		engagements['insights'].append(engaged_dict)
		
	return JsonResponse(json.dumps(engagements), safe=False)

#-------------------------------------------------------------#

def get_post_by_unique_users(mid):
	mc = MongoClient()

        db = mc.olap

        unique_users = {}
        unique_users['_id'] = mid
        unique_users['insights'] = []

        rec = db.post_history.find({"_id":ObjectId(mid)})

	if rec.count() != 1:
                return JsonResponse(json.dumps({"error": "invalid id"}), safe=False)

        for r in rec:
                uni = r

        for ins in uni['insights']:
                uniq = ins['uu']

                uniq_dict = {}
                uniq_dict['engagements'] = uniq

                unique_users['insights'].append(uniq_dict)
	
	return JsonResponse(json.dumps(unique_users), safe=False)

#-------------------------------------------------------------#

def get_comments_by_authors(auth):
	mc = MongoClient()

        db = mc.olap

        author_comments = {}
        author_comments['author'] = auth
        author_comments['insights'] = []

        rec = db.post_history.find({"author": auth})

        for r in rec:
                auth = r

		for ins in auth['insights']:
			comm = ins['comment']

			comm_dict = {}
			comm_dict['engagements'] = comm
			comm_dict['date'] = ins['date']

			author_comments['insights'].append(comm_dict)
	
	return JsonResponse(json.dumps(author_comments), safe=False)

#-------------------------------------------------------------#

def get_engagements_by_authors(auth):
	mc = MongoClient()

        db = mc.olap

        author_engagements = {}
        author_engagements['author'] = auth
        author_engagements['insights'] = []

        rec = db.post_history.find({"author": auth})

        for r in rec:
                eng = r

		for ins in eng['insights']:
			engaged = ins['comment'] + ins['share'] + ins['like']

			engaged_dict = {}
			engaged_dict['engagements'] = engaged
			engaged_dict['date'] = ins['date']

			author_engagements['insights'].append(engaged_dict)
	
	return JsonResponse(json.dumps(author_engagements), safe=False)

