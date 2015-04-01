#Crawl articles from online news sources for NBA

# coding=utf-8

import requests
#import time
from BeautifulSoup import BeautifulSoup
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
#from time import sleep
import sys

def slug_maker(term):
	term=term.lower()
	term=term.replace(' ','-')
	return term

def crawl_page(url):
	while True:
		try:
			#print "Trying to get URL... ",
			r=requests.get(url)
			#print "Got URL!"
			if(r.status_code==404):
				print "Sorry, but the page",url,"does not exist. Exiting."
				return 0
			return r.content
		except Exception as e:
			print e
			print "Retrying."

def fox_article_crawler(url):
	raw=crawl_page(url)
	parsed_url=BeautifulSoup(raw)
	tags=parsed_url.find("div",{"class":"story-tags"})
	if(tags==None):
		tags="<no tags>"
	else:
		tags=tags.findAll("a")
	out=["",""]
	taglist=""
	for tag in tags:
		if(tag.find("span")==-1):
			continue
		s=tag.find("span").contents[0].strip()
		taglist+=s+"-"
	out[0]=taglist
	blurb=parsed_url.find("div",{"class":"story-content without-dateLine"})
	if(blurb==None):
		blurb="<no summary found>"
	else:
		blurb=blurb.find("p")
		blurb=str(blurb)
		blurb=blurb.encode("utf-8")
		re.sub(r'\<.+?\>\s*', '', blurb)
		out[1]=blurb
	return out
	
def fox_parser(content,num):
	count=0
	if(content==0):
		return
	parsed_url=BeautifulSoup(content)
	all_posts=parsed_url.findAll("article")
	for post in all_posts:
		info=post.find("a")
		link=info['href'] #ARTICLE LINK
		title=info.find("h3",{"class":"buzzer-title"}).contents[0]
		title=title.replace(",","")#ARTICLE TITLE
		date=post.find("span",{"class":"buzzer-pubdate"}).contents[0] #ARTICLE DATE
		others=fox_article_crawler(link)
		tags=others[0]
		blurb=others[1]
		blurb=blurb.replace(",","")
		print "POST",count
		print "TITLE:",title
		print "BLURB:",blurb
		print "LINK:",link
		print "TAGS:",tags
		print "TIMESTAMP:",date
		outstr=""
		outstr=title.encode("utf-8")+", "+blurb.encode("utf-8")+", "+link.encode("utf-8")+", "+tags.encode("utf-8")+", "+date.encode("utf-8")+"\n"
		fp=open("outputFoxNews.csv","a")
		fp.write(outstr)
		fp.close()
		count+=1
fox_parser(crawl_page("http://www.foxsports.com/nba/news"),10)