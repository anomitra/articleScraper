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
	
#	CODE FOR CRAWLING THE GUARDIAN	#

def guardian_urlify(slug):
	base="http://www.theguardian.com/football/"
	url=base+slug
	return url

def guardian_image_crawl(url):
	parsed_url=BeautifulSoup(crawl_page(url))
	images=parsed_url.findAll("img",{"itemprop":"contentURL representativeOfPage"})
	if(len(images)==0):
		return "<no image>"
	return images[0]['src'][2:]
def guardian_parse(content,num):
	if(content==0):
		return
	parsed_url=BeautifulSoup(content)
	all_posts=parsed_url.findAll("a",{ "data-link-name" : "article" })
	timestamps=parsed_url.findAll("time",{ "class" : "fc-item__timestamp" })
	count=0
	while (count<num):
		post=all_posts[count*2+1]
		stamp=timestamps[count]
		count=count+1
		title=post.contents[0]
		link=post['href']
		img=guardian_image_crawl(link)
		time=stamp['datetime']
		#print post
		#print "-------------------------------------"
		print "POST",count
		print "TITLE:",title
		print "LINK:",link
		print "IMAGE:",img
		print "TIMESTAMP:",time
		print "-------------------------------------"
		outstr=title+", "+link+", "+img+", "+time+"\n"
		outstr=outstr.encode("utf-8")
		fp=open("output.csv","a")
		fp.write(outstr)
	fp.close()

#	CODE FOR CRAWLING THE MIRROR	#

def mirror_urlify(slug):
	base1="http://www.mirror.co.uk/all-about/"
	base2="?all=true"
	url=base1+slug+base2
	return url

def mirror_parse(content,num):
	if(content==0):
		return
	parsed_url=BeautifulSoup(content)
	#firstpost=parsed_url.findAll("div",{"class":"article sa-teaser clearfix secondary"})
	#print posts
	#all_posts=parsed_url.findAll("div",{"class":"article sa-teaser clearfix ma-teaser"})
	#all_posts.insert(0,firstpost)
	timestamps=parsed_url.findAll("time")
	all_posts=parsed_url.findAll("div",{"class":"teaser-info"})
	count=0
	while (count<num):
		post=all_posts[count]
		stamp=timestamps[count]
		#print post
		title=post.find("a").contents[0]
		title=title.replace(',','')
		link=post.find("a")['href']
		#img=post.find("img")['src']
		time=stamp['datetime']
		count=count+1
		print "POST",count
		print "TITLE:",title
		print "LINK:",link
		#print "IMAGE:",img
		print "TIMESTAMP:",time
		img=""
		print "-------------------------------------"
		outstr=title+", "+link+", "+img+", "+time+"\n"
		outstr=outstr.encode("utf-8")
		fp=open("outputMirror.csv","a")
		fp.write(outstr)
	fp.close()
#name=raw_input("Enter the topic: ")
#num=int(raw_input("Enter the number of articles: "))
name="Wayne Rooney"
num=5
guardian_parse(crawl_page(guardian_urlify(slug_maker(name))),num)
mirror_parse(crawl_page(mirror_urlify(slug_maker(name))),num)
