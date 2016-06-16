'Creates two csv data files parsed from existing JSON data'

from bs4 import BeautifulSoup
import urllib2
import json
import csv
import time
import requests
import os
import unicodedata
import logging

# categories array to be fetched from the ScoopWhoop url source page of each post
categories = []

# 2 D array containing array of keywords of each post
keywords = []

def get_page_links(data):
	' Returns a list of ScoopWhoop page urls to be used to get categories and keywords '

	pages = []

	# Getting page url from each post
	for d in data:
		pages.append(d['link'])

	return pages

#---------------------------------------------------------------------------------------------------------------------------------------------#

def get_data_from_post(pages):
	' Fills global arrays categories[] and keywords[] from page URLs '

	global categories, keywords, no_of_images, images

	passes = 0

	for page in pages:
		# Temporary string of keywords which is to be stripped and splitted at commas to get a list of keywords
		keys = ""

		response = urllib2.urlopen(page)

		source = response.read()

		soup = BeautifulSoup(source, 'html.parser')

		# Iterating to get categories array and temporary string of keywords
		for meta in soup.find_all('meta'):
			if(meta.get('property')=='category'):
				categories.append(str(meta.get('content')))

			if(meta.get('name')=='keywords'):
				keys = str(meta.get('content'))

		if len(categories) != passes + 1:
			categories.append('others'.encode("utf-8"))

		# Process temporary string by List Comprehension
		tt = [x.strip() for x in keys.split(',')]

		keywords.append(tt)

		passes = passes + 1

#---------------------------------------------------------------------------------------------------------------------------------------------#

def get_index_from_json(data, key, value):
	' Returns an index reading JSON data to find the value at the particular key '

	# Searching key-value pair in all indices
	for idx in xrange( len(data['insights']['data']) ):
		if data['insights']['data'][idx][key] == value:
			return idx
	
def get_int_month(month_str):
	' Returns from 1-12 the month number from a three letter coded string '	

	months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

	for i in range(len(months)):
		if month_str == months[i]:
			return i+1

def process_pub_date(pub_date):
	' Returns a list containing year month day hour mins extracted from a string of published date'

	ymdhm = []
	ymdhm.append(int(pub_date[8:12]))
	ymdhm.append(get_int_month(pub_date[0:3]))
	ymdhm.append(int(pub_date[4:6]))
	ymdhm.append(int(pub_date[16:18]))
	ymdhm.append(int(pub_date[19:21]))

	return ymdhm


def write_into_csv(data, pdata, owriter, owriter1):
	' Writes into two csv files data.csv and keywords_data.csv parsing the JSON data file'

        owriter.writerow(['id','name','message','category', 'author', 'likes', 'shares', 'comments', 'ctr', 'year', 'month', 'day','no_of_images', 'head_len', 'no_of_abusive_words'])
	owriter1.writerow(['id', 'keywords', 'likes', 'shares', 'comments', 'ctr'])

	# Key and Search Pattern to search for the index
	key = 'name'
	search_pattern = "post_stories_by_action_type"

        category_idx=0
	row = 0

	f1 = open('abusive.txt')
        abusive_words = f1.read()
        abusive_words = abusive_words.split('\n')
        f1.close()

	# Fill data.csv rows for each post
        for i in range(len(data)):
		ctr = calc_ctr(data[i])
	
		# Use this index value to get likes, comments and shares of each post
	        idx = get_index_from_json(data[i], key, search_pattern)

		if 'name' in data[i].keys():
                        name = data[i]['name']
			name = unicodedata.normalize('NFKD', name).encode('ascii','ignore')
                else:
                        name = ''

		if 'message' in data[i].keys():
			message = data[i]['message']
			message = unicodedata.normalize('NFKD', message).encode('ascii','ignore')
		else:
			message = ''

		if 'like' in data[i]['insights']['data'][idx]['values'][0]['value'].keys():
                        like = data[i]['insights']['data'][idx]['values'][0]['value']['like']
                else:
                        like = 0


		if 'share' in data[i]['insights']['data'][idx]['values'][0]['value'].keys():
                        share = data[i]['insights']['data'][idx]['values'][0]['value']['share']
                else:
                        share = 0

		if 'comment' in data[i]['insights']['data'][idx]['values'][0]['value'].keys():
                        comment = data[i]['insights']['data'][idx]['values'][0]['value']['comment']
                else:
                        comment = 0

		if pdata[i]['status']=="1":	
			ymdhm = process_pub_date(pdata[i]['data']['pub_date'])
			year = ymdhm[0]
			month = ymdhm[1]
			day = ymdhm[2]
			hour = ymdhm[3]
			mins = ymdhm[4]
			author = pdata[i]['userData'][0]['display_name']

			source = pdata[i]["data"]['article_content']

	                soup = BeautifulSoup(source, 'html.parser')

			content = soup
			
			if soup.table:
				soup.table.decompose()

        	        images = soup.find_all('img')

                	no_of_images = len(images)

			videos = soup.find_all('iframe')

			no_of_videos = len(videos)

			head_len = len(pdata[i]['data']['title'])
			
			ab_words = []
			
			con = soup.get_text()
                        con = con.split()

                        for word in con :
                                if word in abusive_words:
                                        ab_words.append(word)

                        no_of_abusive_words = len(ab_words)


		else:
			year = 0
			month = 0
			day = 0
			hour = 0
			mins = 0
			author = 'Unknown'
			head_len = 0
			no_of_images = 0
			no_of_videos = 0
			no_of_abusive_words = 0

		owriter.writerow([
				data[i]['id'],
				name,
				message,
				categories[category_idx],
				author,
				like,
				share, 
				comment, 
				ctr,
				year,
				month,
				day,
				hour,
				mins,
				no_of_images,
				no_of_videos,
				head_len,
				no_of_abusive_words])
		
		for column in xrange(len(keywords[row])):
                        owriter1.writerow([
                                        data[i]['id'],
                                        keywords[row][column],
					like,
                                	share,   
                                	comment, 
                                	ctr])

		row = row + 1
                category_idx = category_idx + 1

#---------------------------------------------------------------------------------------------------------------------------------------------#

def calc_ctr(d):
	' Returns Click-Through Rate i.e. clicks per post reach rate '

	ctr = 0

	# Getting index to know the count of post reaches
	idx = get_index_from_json(d, 'name', 'post_impressions_unique')
	
	if d['insights']['data'][idx]['values'][0]['value']:
		reach = d['insights']['data'][idx]['values'][0]['value']
	else:
		reach=0

	sum_clicks = 0

	# Getting index to know the count of different type of clicks
	idx = get_index_from_json(d, 'name', 'post_consumptions_by_type')

	for clicks in d['insights']['data'][idx]['values'][0]['value']:
		sum_clicks = float(d['insights']['data'][idx]['values'][0]['value'][clicks]) + sum_clicks


	if sum_clicks==0 and reach==0:
		ctr =0
	else:    
		ctr = format((sum_clicks/reach)*100, '.2f')

	return ctr

#---------------------------------------------------------------------------------------------------------------------------------------------#

def process_link(tmp):
	' Returns the stripped content from the link of the post '

	tmp = tmp[26:]

	lc = -1
	for i in range(len(tmp)):
		if i!=len(tmp)-1:
			if tmp[i]=='/' and tmp[i+1]=='?':
				lc = i
				break

		elif tmp[i]=='/':
			lc = i

	if lc==-1:
		lc = len(tmp)

	tmp = tmp[:lc]

	return tmp

if __name__== '__main__':
	while True:
	
		logging.basicConfig(filename='api.log', level=logging.DEBUG)
 
     		logging.debug('loading JSON data. . .\n')
 
 		try:
	                '''r= requests.get('http://10.2.1.35:8087/')
 
        	        data = r.json()'''		

			with open('data.json') as f:
				data = json.load(f)

			post_data = []
			for d in data:
				tmp = d['link']
				if 'http://www.scoopwhoop.com' not in tmp:
		               		post_data.append({"status":"0"})
					continue
			
				link = process_link(tmp)
				post_r = requests.get('http://www.scoopwhoop.com/api/v1/'+link)
				post_data.append(post_r.json())

			csv_file = open('fb_posts_data.csv','w')
			csv_file1 = open('keywords_data.csv', 'w')

			owriter = csv.writer(csv_file)
			owriter1 = csv.writer(csv_file1)

			logging.debug('get page links. . .\n')

			pages = get_page_links(data)

			logging.debug('loading categories and keywords. . .\n')

			get_data_from_post(pages)

			logging.debug('writing into csv files. . .\n')

			write_into_csv(data, post_data, owriter, owriter1)

			logging.debug('data loaded successfully!\n')

			csv_file.close()
			csv_file1.close()

			os.system('python prep_data.py')

		except Exception as e:
			logging.error(str(e))

		time.sleep(7200)
