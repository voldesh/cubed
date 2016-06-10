'Creates two csv data files parsed from existing JSON data'

from bs4 import BeautifulSoup
import urllib2
import json
import csv
import time
import requests
import os
import unicodedata

# categories array to be fetched from the ScoopWhoop url source page of
# each post
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


def get_categories_keywords(pages):
    ' Fills global arrays categories[] and keywords[] from page URLs '

    global categories, keywords

    passes = 0

    for page in pages:
        # Temporary string of keywords which is to be stripped and splitted at
        # commas to get a list of keywords
        keys = ""

        response = urllib2.urlopen(page)

        source = response.read()

        soup = BeautifulSoup(source, 'html.parser')

        # Iterating to get categories array and temporary string of keywords
        for meta in soup.find_all('meta'):
            if(meta.get('property') == 'category'):
                categories.append(str(meta.get('content')))

            if(meta.get('name') == 'keywords'):
                keys = str(meta.get('content'))

        if len(categories) != passes + 1:
            categories.append('others'.encode("utf-8"))

        # Process temporary string by List Comprehension
        tt = [x.strip() for x in keys.split(',')]

        keywords.append(tt)

        passes = passes + 1

        print categories[passes - 1]

        print "Completed " + str(passes)

#---------------------------------------------------------------------------------------------------------------------------------------------#


def get_index_from_json(data, key, value):
    ' Returns an index reading JSON data to find the value at the particular key '

    # Searching key-value pair in all indices
    for idx in xrange(len(data['insights']['data'])):
        if data['insights']['data'][idx][key] == value:
            return idx


def write_into_csv(data, owriter, owriter1):
    ' Writes into two csv files data.csv and keywords_data.csv parsing the JSON data file'

    owriter.writerow(['id', 'name', 'message', 'category',
                      'likes', 'shares', 'comments', 'ctr'])
    owriter1.writerow(['id', 'keywords', 'likes', 'shares', 'comments', 'ctr'])

    # Key and Search Pattern to search for the index
    key = 'name'
    search_pattern = "post_stories_by_action_type"

    category_idx = 0
    row = 0

    # Fill data.csv rows for each post
    for d in data:
        ctr = calc_ctr(d)

        # Use this index value to get likes, comments and shares of each post
        idx = get_index_from_json(d, key, search_pattern)

        if 'name' in d.keys():
            name = d['name']
            name = unicodedata.normalize(
                'NFKD', name).encode('ascii', 'ignore')
        else:
            name = ''

        if 'message' in d.keys():
            message = d['message']
            message = unicodedata.normalize(
                'NFKD', message).encode('ascii', 'ignore')
        else:
            message = ''

        if 'like' in d['insights']['data'][idx]['values'][0]['value'].keys():
            like = d['insights']['data'][idx]['values'][0]['value']['like']
        else:
            like = 0

        if 'share' in d['insights']['data'][idx]['values'][0]['value'].keys():
            share = d['insights']['data'][idx]['values'][0]['value']['share']
        else:
            share = 0

        if 'comment' in d['insights']['data'][idx]['values'][0]['value'].keys():
            comment = d['insights']['data'][idx][
                'values'][0]['value']['comment']
        else:
            comment = 0

        owriter.writerow([
            d['id'],
            name,
            message,
            categories[category_idx],
            like,
            share,
            comment,
            ctr])

        for column in xrange(len(keywords[row])):
            owriter1.writerow([
                d['id'],
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
        reach = 0

    sum_clicks = 0

    # Getting index to know the count of different type of clicks
    idx = get_index_from_json(d, 'name', 'post_consumptions_by_type')

    for clicks in d['insights']['data'][idx]['values'][0]['value']:
        sum_clicks = float(d['insights']['data'][idx]['values'][
                           0]['value'][clicks]) + sum_clicks
        '''other_clicks = d['insights']['data'][idx]['values'][0]['value']['other clicks']
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

		click = float(other_clicks + link_clicks + photo_views)'''

    if sum_clicks == 0 and reach == 0:
        ctr = 0
    else:
        ctr = format((sum_clicks / reach) * 100, '.2f')

    return ctr

#---------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    while True:
        print 'loading JSON data. . .\n'

        r = requests.get('http://172.18.2.209:8090/')
        '''with open('fb_posts.json') as f:
			data = json.load(f)'''

        data = r.json()

        csv_file = open('fb_posts_data.csv', 'w')
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

        csv_file.close()
        csv_file1.close()

        os.system('python prep_data.py')

        time.sleep(7200)
