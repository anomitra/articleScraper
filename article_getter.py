#Crawl articles from online news sources

import requests
#import time
from BeautifulSoup import BeautifulSoup
import re
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
#from time import sleep
import sys

def slug_maker(term):
	term=term.lower()
	term=term.replace(' ','-')
	return term

def guardian_urlify(slug):
	base="http://www.theguardian.com/football/"
	url=base+slug
	return url
	
def crawl_page(url):
	while True:
		try:
			print "Trying to get URL... ",
			r=requests.get(url)
			print "Got URL!"
			return r.content
		except Exception as e:
			print e
			sleep(2)
			print "Retrying."

def guardian_parse(content,num):
	parsed_url=BeautifulSoup(content)
	all_posts=parsed_url.findAll("a",{ "data-link-name" : "article" })
	timestamps=parsed_url.findAll("time",{ "class" : "fc-item__timestamp" })
	count=0
	while (count<num):
		post=all_posts[count*2+1]
		stamp=timestamps[count]
		count=count+1
		#print post
		#print "-------------------------------------"
		print "POST",count
		print "TITLE:",post.contents[0]
		print "LINK:",post['href']
		print "TIMESTAMP:",stamp['datetime']
		print "-------------------------------------"

name=raw_input("Enter the topic:")
num=int(raw_input("Enter the number of articles:"))

guardian_parse(crawl_page(guardian_urlify(slug_maker(name))),num)
