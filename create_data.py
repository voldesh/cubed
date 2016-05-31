'Creates two csv data files parsed from existing JSON data'

from bs4 import BeautifulSoup
import urllib2
import json
import csv
import time

# categories array to be fetched from the ScoopWhoop url source page of each post
categories = []

# 2 D array containing array of keywords of each post
keywords = []

# TODO: get page links through json

def get_page_links(data):
	' Returns a list of ScoopWhoop page urls to be used to get categories and keywords '

	# Hard coded the 5 page urls for now
	pages = ['http://www.scoopwhoop.com/Aishwaryas-Famous-Purple-Lips-On-Other-Bollywood-Actresses-?ref=social&type=fb&b=0','http://www.scoopwhoop.com/ghanta-awards-bollywood-2016/?ref=social&type=fb&b=0','http://www.scoopwhoop.com/Meghana-Erande-Voice-Behind-Ninja-Hattori-Famous-Cartoon-Characters/?ref=social&type=fb&b=0','http://www.scoopwhoop.com/Mouni-Roy-Goa-Trip/?ref=social&type=fb&b=0','http://www.scoopwhoop.com/Anshuman-In-Jab-We-Met-Tollywood-Actor/?ref=social&type=fb&b=0']

	return pages

	'''pages = []

	# Getting page url from each post
	for d in data:
		pages.append('')

	return pages'''

#---------------------------------------------------------------------------------------------------------------------------------------------#

def get_categories_keywords(pages):
	' Fills global arrays categories[] and keywords[] from page URLs '

	global categories, keywords

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

		# Process temporary string by List Comprehension
		tt = [x.strip() for x in keys.split(',')]

		keywords.append(tt)

#---------------------------------------------------------------------------------------------------------------------------------------------#

def get_index_from_json(data, key, value):
	' Returns an index reading JSON data to find the value at the particular key '

	# Searching key-value pair in all indices
	for idx in xrange( len(data['insights']['data']) ):
		if data['insights']['data'][idx][key] == value:
			return idx
	

def write_into_csv(data, owriter, owriter1):
	' Writes into two csv files data.csv and keywords_data.csv parsing the JSON data file'

        owriter.writerow(['id','name','description','message','category', 'likes', 'shares', 'comments', 'ctr'])
	owriter1.writerow(['id', 'keywords', 'likes', 'shares', 'comments', 'ctr'])

	# Key and Search Pattern to search for the index
	key = 'name'
	search_pattern = "post_stories_by_action_type"

        category_idx=0
	row = 0

	# Fill data.csv rows for each post
        for d in data:
		ctr = calc_ctr(d)
	
		# Use this index value to get likes, comments and shares of each post
	        idx = get_index_from_json(d, key, search_pattern)

                owriter.writerow([
				d['id'],
				d['name'].encode("utf-8"), 
				d['description'].encode("utf-8"),
				d['message'].encode("utf-8"),
 				categories[category_idx],
				d['insights']['data'][idx]['values'][0]['value']['like'], 
				d['insights']['data'][idx]['values'][0]['value']['share'], 
				d['insights']['data'][idx]['values'][0]['value']['comment'], 
				ctr])

		for column in xrange(len(keywords[row])):
                        owriter1.writerow([
                                        d['id'],
                                        keywords[row][column],
					d['insights']['data'][idx]['values'][0]['value']['like'], 
                                	d['insights']['data'][idx]['values'][0]['value']['share'], 
                                	d['insights']['data'][idx]['values'][0]['value']['comment'], 
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

	click = 0

	# Getting index to know the count of different type of clicks
	idx = get_index_from_json(d, 'name', 'post_consumptions_by_type')

	if d['insights']['data'][idx]['values'][0]['value']:
		other_clicks = d['insights']['data'][idx]['values'][0]['value']['other clicks']
		link_clicks = d['insights']['data'][idx]['values'][0]['value']['link clicks']
		photoviews = d['insights']['data'][idx]['values'][0]['value']
		if 'photo view' in photoviews:
		    photo_views = d['insights']['data'][idx]['values'][0]['value']['photo view']
		else:
		    photo_views = 0

		click = float(other_clicks + link_clicks + photo_views)
	else:
		other_clicks = 0
		link_clicks = 0
		photo_views = 0

		click = float(other_clicks + link_clicks + photo_views)

	if click==0 and reach==0:
		ctr =0
	else:    
		ctr = format((click/reach)*100, '.2f')

	return ctr

#---------------------------------------------------------------------------------------------------------------------------------------------#

if __name__== '__main__':
	
	s_time = time.time()

	print 'loading JSON data. . .\n'

	with open('fb_posts.json') as data_file:    
		data = json.load(data_file)


	csv_file = open('fb_posts_data.csv','w')
	csv_file1 = open('keywords_data.csv', 'w')

	owriter = csv.writer(csv_file)
	owriter1 = csv.writer(csv_file1)

	print 'get page links. . .\n'

	pages = get_page_links(data)

	print 'loading categories and keywords. . .\n'

	get_categories_keywords(pages)

	print 'writing into csv files. . .\n'

	write_into_csv(data, owriter, owriter1)

	print 'data loaded successfully!\n'


	e_time = time.time()

	t_time = format(e_time - s_time, '.2f')

	print 'Total Time Taken : ' + str(t_time) + ' seconds\n'
