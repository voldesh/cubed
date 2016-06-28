import os.path
BASE = os.path.dirname(os.path.abspath(__file__))

from cubes import Workspace, Cell, PointCut
from datetime import datetime, timedelta
import sys
import json
from django.http import JsonResponse

#-------------------------------------------------------------#
workspace = Workspace()
workspace.register_default_store("sql", url="sqlite:///"+os.path.join(BASE,"myData.sqlite"))
workspace.import_model(os.path.join(BASE,"modal.json"))

browser = workspace.browser("FB_POSTS_DATA")

#-------------------------------------------------------------#

d =  datetime.now() - timedelta(days=1)

cut = PointCut("pub_date", [d.year, d.month, d.day-6], None)

cell = Cell(browser.cube, cuts = [cut])

#-------------------------------------------------------------#

def get_post_by_shares():
	result = browser.aggregate(cell, drilldown=["name"])

	shares = []

	for row in result.table_rows("name"):
                total_shares = row.record["total_shares"]

                post_by_share = {}
                post_by_share["date"] = str(d)
                post_by_share["post_name"] = row.label
                post_by_share["total_shares"] = total_shares

                shares.append(post_by_share)

    	return JsonResponse(json.dumps(shares), safe=False)


#------------------------------------------------------------#

def get_post_by_engagements():
	result = browser.aggregate(cell, drilldown=["name"])

        engagements = []
	
	for row in result.table_rows("name"):
		total_engagements = row.record["total_likes"] + row.record["total_shares"] + row.record["total_comments"]

		post_by_engagements = {}
                post_by_engagements["date"] = str(d)
                post_by_engagements["post_name"] = row.label
                post_by_engagements["total_engagements"] = total_engagements

		engagements.append( post_by_engagements )

	return JsonResponse(json.dumps(engagements), safe=False)

#-------------------------------------------------------------#

def get_post_by_unique_users():
	result = browser.aggregate(cell, drilldown=["name"])

        unique_users = []

	for row in result.table_rows("name"):
		total_newusers = row.record['total_newusers']

		post_by_unique_users = {}
                post_by_unique_users["date"] = str(d)
                post_by_unique_users["post_name"] = row.label
                post_by_unique_users["total_newusers"] = total_newusers

		unique_users.append(post_by_unique_users)

	return JsonResponse(json.dumps(unique_users), safe=False)

#-------------------------------------------------------------#

def get_comments_by_authors():
	result = browser.aggregate(cell, drilldown=["author"])

	author_comments = []

	for row in result.table_rows("author"):
		total_comments = row.record["total_comments"]
		
		comments_by_author = {}
		comments_by_author["date"] = str(d)
		comments_by_author["author"] = row.label
		comments_by_author["total_comments"] = total_comments

		author_comments.append( comments_by_author )

	return JsonResponse(json.dumps(author_comments), safe=False)

#-------------------------------------------------------------#

def get_engagements_by_authors():
	result = browser.aggregate(cell, drilldown=["author"])
        
        author_engagements = []

	for row in result.table_rows("author"):

		total_engagements = row.record["total_likes"] + row.record["total_shares"] + row.record["total_comments"]

		engagements_by_author = {}
                engagements_by_author["date"] = str(d)
                engagements_by_author["author"] = row.label
                engagements_by_author["total_engagements"] = total_engagements

                author_engagements.append( engagements_by_author )

	return JsonResponse(json.dumps(author_engagements), safe=False)

