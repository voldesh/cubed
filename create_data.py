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
from urlparse import urlparse

def load_data(file_name):
    ' Returns a list from csv data '
    csv_data = []
    with open(file_name, 'rb') as f:
        data = csv.reader(f)
        for d in data:
            csv_data.append(d)

    return csv_data

#---------------------------------------------------------------------------------------------------------------------------------------------#

# categories array to be fetched from the ScoopWhoop url source page of
# each post
categories = []

# 2 D array containing array of keywords of each post
keywords = []

#---------------------------------------------------------------------------------------------------------------------------------------------#

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

#---------------------------------------------------------------------------------------------------------------------------------------------#


def get_index_from_json(data, key, value):
    ' Returns an index reading JSON data to find the value at the particular key '

    # Searching key-value pair in all indices
    for idx in xrange(len(data['insights']['data'])):
        if data['insights']['data'][idx][key] == value:
            return idx


def get_int_month(month_str):
    ' Returns from 1-12 the month number from a three letter coded string '

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for i in range(len(months)):
        if month_str == months[i]:
            return i + 1


def process_pub_date(pub_date):
    ' Returns a list containing year month day hour mins extracted from a string of published date'

    ymdhm = []
    ymdhm.append(int(pub_date[0:4]))
    ymdhm.append(get_int_month(pub_date[5:7]))
    ymdhm.append(int(pub_date[8:10]))
    ymdhm.append(int(pub_date[11:13]))
    ymdhm.append(int(pub_date[14:16]))

    return ymdhm

def get_author(pdata, i):
    ' Returns author of a post '

    return pdata[i]['userData'][0]['display_name']

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

    if sum_clicks == 0 and reach == 0:
        ctr = 0
    else:
        ctr = format((sum_clicks / reach) * 100, '.2f')

    return ctr

def get_no_of_abusive_words(soup):
    ' Returns number of abusive words in article content '

    f1 = open('abusive.txt')

    abusive_words = f1.read()
    abusive_words = abusive_words.split('\n')

    ab_words = []

    con = soup.get_text()
    con = con.split()

    for word in con:
        if word in abusive_words:
            ab_words.append(word)

    f1.close()

    return len(ab_words)

def get_article_content(pdata, i):
    return pdata[i]["data"]['article_content']

def get_no_of_images(soup):
    ' Returns number of images in a post '

    images = soup.find_all('img')

    no_of_images = len(images)

    return no_of_images

def get_no_of_videos(soup):
    ' Returns number of videos in a post '

    videos = soup.find_all('iframe')

    no_of_videos = len(videos)

    return no_of_videos

def get_heading_length(pdata, i):
    ' Returns number of characters in the title of a post '

    return len(pdata[i]['data']['title'])

def get_ga_data(ga_data, data, i):
    ga_data_ = []    

    link = data[i]['link']
    link = urlparse(link).path.strip('/')

    pageviews = 0
    uniquePageviews = 0
    avgTimeOnPage = 0
    newUsers = 0
    bounceRate = 0

    print i
    print link

    c = 0
    for j in xrange(1,len(ga_data)) :
        slug = urlparse(ga_data[j][0])

	path = slug.path.strip('/')

        if path in link and path!='':
	    c = c + 1
	    if c==1:
	    	print path
            pageviews = pageviews + int(ga_data[j][1])
	    uniquePageviews = uniquePageviews + int(ga_data[j][2])
            avgTimeOnPage = avgTimeOnPage + float(ga_data[j][3])
	    newUsers = newUsers + int(ga_data[j][4])
            bounceRate = bounceRate + float(ga_data[j][5])

    ga_data_.append(pageviews)
    ga_data_.append(uniquePageviews)
    ga_data_.append(avgTimeOnPage) 
    ga_data_.append(newUsers)
    ga_data_.append(bounceRate)

    return ga_data_


def write_into_csv(data, pdata, owriter, owriter1, ga_data_csv):
    ' Writes into two csv files fb_posts_data.csv and keywords_data.csv parsing the JSON data file'

    owriter.writerow(['id', 'name', 'category', 'author', 'likes', 'shares', 'comments',
                      'ctr', 'year', 'month', 'day', 'no_of_images', 'head_len', 'no_of_abusive_words', 
		      'pageviews', 'uniquePageviews', 'avgTimeOnPage', 'newUsers', 'bounceRate'])
    owriter1.writerow(['id', 'keywords', 'likes', 'shares', 'comments', 'ctr'])

    # Key and Search Pattern to search for the index
    key = 'name'
    search_pattern = "post_stories_by_action_type"

    category_idx = 0
    row = 0
	
    ga_data = load_data(ga_data_csv)

    # Fill data.csv rows for each post
    for i in range(len(data)):
        ctr = calc_ctr(data[i])

        # Use this index value to get likes, comments and shares of each post
        idx = get_index_from_json(data[i], key, search_pattern)

        if 'name' in data[i].keys():
            name = data[i]['name']
            name = unicodedata.normalize(
                'NFKD', name).encode('ascii', 'ignore')
        else:
            name = ''

        if 'like' in data[i]['insights']['data'][idx]['values'][0]['value'].keys():
            like = data[i]['insights']['data'][
                idx]['values'][0]['value']['like']
        else:
            like = 0

        if 'share' in data[i]['insights']['data'][idx]['values'][0]['value'].keys():
            share = data[i]['insights']['data'][
                idx]['values'][0]['value']['share']
        else:
            share = 0

        if 'comment' in data[i]['insights']['data'][idx]['values'][0]['value'].keys():
            comment = data[i]['insights']['data'][
                idx]['values'][0]['value']['comment']
        else:
            comment = 0

	ga_data_ = get_ga_data(ga_data, data, i)

	pageviews = ga_data_[0]
	uniquePageviews = ga_data_[1]
	avgTimeOnPage = ga_data_[2]
	newUsers = ga_data_[3]
    	bounceRate = ga_data_[4]
	
	ymdhm = process_pub_date(data[i]['created_time'])
        year = ymdhm[0]
        month = ymdhm[1]
        day = ymdhm[2]
        hour = ymdhm[3]
        mins = ymdhm[4]
	
        if pdata[i]['status'] == "1":
                        
            author = get_author(pdata, i)

            source = get_article_content(pdata, i)

            soup = BeautifulSoup(source, 'html.parser')

            content = soup

            if soup.table:
                soup.table.decompose()

            no_of_images = get_no_of_images(soup)

            no_of_videos = get_no_of_videos(soup)

            head_len = get_heading_length(pdata, i)

            no_of_abusive_words = get_no_of_abusive_words(soup)

        else:
            author = 'Unknown'
            head_len = 0
            no_of_images = 0
            no_of_videos = 0
            no_of_abusive_words = 0	
	   	
        owriter.writerow([
            data[i]['id'],
            name,
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
            no_of_abusive_words,
	    pageviews,
	    uniquePageviews,
	    avgTimeOnPage,
	    newUsers,
	    bounceRate])

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

if __name__ == '__main__':
    while True:

        logging.basicConfig(filename='api.log', level=logging.DEBUG)

        logging.debug('\nloading JSON data. . .\n')

        try:
            start_time = time.time()

            '''r= requests.get('http://10.2.1.35:8087/')

            data = r.json()'''

            '''with open('old_data.json') as f:
                old_dt = json.load(f)'''

            with open('data1.json') as f:
                data = json.load(f)

            '''for d in old_dt:
                data.append(d)'''

            post_data = []
            for d in data:
                link = d['link']

		parsed_uri = urlparse( link )
		domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

                if 'facebook' in domain:
                    post_data.append({"status": "0"})
                    continue

                link = parsed_uri.path
		if link[len(link)-1] == '/':
			link = link[:len(link)-1]
		#print link
                post_r = requests.get(
                    'http://www.scoopwhoop.com/api/v1/' + link)
                post_data.append(post_r.json())

            ga_data_csv = "csv_latest.csv"

            csv_file = open('fb_posts_data.csv', 'w')
            csv_file1 = open('keywords_data.csv', 'w')

            owriter = csv.writer(csv_file)
            owriter1 = csv.writer(csv_file1)

            logging.debug('get page links. . .\n')

            pages = get_page_links(data)

            logging.debug('loading categories and keywords. . .\n')

            get_data_from_post(pages)

            logging.debug('writing into csv files. . .\n')

            write_into_csv(data, post_data, owriter, owriter1, ga_data_csv)

            logging.debug('data loaded successfully!\n')

            csv_file.close()
            csv_file1.close()

            logging.debug('Time elapsed : ' + str(time.time() - start_time) + ' s.\n')

            os.system('python prep_data.py add')

        except Exception as e:
            logging.error(str(e))

        time.sleep(7200)
