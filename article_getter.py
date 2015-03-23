#Crawl articles from online news sources

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
	
#	CODE FOR CRAWLING THE GUARDIAN	#

def guardian_urlify(slug):
	base="http://www.theguardian.com/football/"
	url=base+slug
	return url

def guardian_article_crawl(url):
	parsed_url=BeautifulSoup(crawl_page(url))
	out=["","","",""]
	
	#IMAGE
	
	images=parsed_url.findAll("img",{"itemprop":"contentURL representativeOfPage"})
	if(len(images)==0):
		out[0]="<no image>".encode("utf-8")
	else:
		out[0]=images[0]['src'][2:].encode("utf-8")
	
	#TITLE
	
	title=parsed_url.find("title")
	out[1]=title.contents[0].replace(',','').encode("utf-8")
	
	#TIMESTAMP
	
	out[2]=parsed_url.find("time",{"itemprop":"datePublished"})['datetime'].encode("utf-8")
	
	#TAGS
	
	tags=parsed_url.find("ul",{"class":"keyword-list inline-list"})
	if(tags==None):
		out[3]="<no tags>"
		return out
	tags=tags.findAll("li",{"class":"inline-list__item "})
	#print tags
	taglist=""
	for tag in tags:
		s=tag.find("a",{"itemprop":"keywords"}).contents[0].strip()
		#print s
		taglist+=s+"-"
	out[3]=taglist[0:len(taglist)-1].encode("utf-8")

	return out
	
def guardian_parser(content,num):
	if(content==0):
		return
	parsed_url=BeautifulSoup(content)
	all_posts=parsed_url.findAll("div",{ "class" : "fc-item__container" })
	#timestamps=parsed_url.findAll("time",{ "class" : "fc-item__timestamp" })
	count=0
	#print "NUM IS",num
	while (count<num):
		post=all_posts[count]
		#stamp=timestamps[count]
		count=count+1
		link=post.find("a",{"class":"u-faux-block-link__overlay"})['href']
		out=guardian_article_crawl(link)
		#time=stamp['datetime']
		#print post
		#print "-------------------------------------"
		print "POST",count
		print "TITLE:",out[1]
		print "LINK:",link
		print "IMAGE:",out[0]
		print "TIMESTAMP:",out[2]
		print "TAGS:",out[3] 
		print "-------------------------------------"
		outstr=out[1]+", "+link.encode("utf-8")+", "+out[0]+", "+out[2]+", "+out[3]+"\n"
		#outstr=outstr
		fp=open("outputGuardian.csv","a")
		fp.write(outstr)
	fp.close()

#	CODE FOR CRAWLING THE MIRROR	#

def mirror_urlify(num):
	base="http://www.mirror.co.uk/sport/football/news/?pageNumber="
	base+=str(num)
	return base

def mirror_article_crawler(url):
	raw=crawl_page(url)
	parsed_url=BeautifulSoup(raw)
	out=["","",""]
	info=parsed_url.find("div",{"class":"related-widget"})
	info=info.findAll("a")
	if(len(info)==0):
		out[0]="Uncategorized"
	tags=""
	#print "TAGS INCOMING!!"
	for tag in info:
		#print tag.string.strip(',').strip('\n'),
		tags+=tag.contents[0]+"-"
	#print tags
	out[0]=tags[0:len(tags)-1]
	img=parsed_url.find("div",{"class":"image-credit-wrapper"})
	if(img==None): out[1]="<no image>"
	else: 
		img=img.find("img")
		out[1]=img['src']
	
	return out
	
def mirror_parser(content,num,page,total_posts):
	count=0
	if(content==0):
		return
	parsed_url=BeautifulSoup(content)
	all_posts=parsed_url.findAll("div",{"class":"teaser-info"})
	for post in all_posts:
		#print post
		info=post.find("a")
		link=info['href']
		title=info.contents[0]
		title=title.replace(',','').strip()
		# SKIPPING LIVE MATCH ARTICLES
		skip="Live: English Barclays Premier League"
		if(fuzz.partial_ratio(title,skip)==100):
			continue
		blurb=post.find("p").contents[0]
		blurb=blurb.replace(',','').strip()
		time=post.find("time")['datetime']
		data=mirror_article_crawler(link)
		img=str(data[1])
		data[0]=data[0]
		count+=1
		print "POST",count
		print "TITLE:",title
		print "BLURB:",blurb
		print "LINK:",link
		print "IMAGE:",img
		print "TIMESTAMP:",time
		print "TAGS:",data[0]
		total_posts+=1
		print "COUNT ",count,"TOTAL POSTS ",total_posts,"NUM",num
		outstr=""
		outstr=title.encode("utf-8")+", "+blurb.encode("utf-8")+", "+link.encode("utf-8")+", "+img.encode("utf-8")+", "+data[0].encode("utf-8")+", "+time.encode("utf-8")+"\n"
		outstr=outstr
		fp=open("outputMirror.csv","a")
		fp.write(outstr)
		fp.close()
		if(count==num):
			return
	page+=1
	mirror_parser(crawl_page(mirror_urlify(page)),num-total_posts,page,total_posts)

"""def mirror_urlify(slug):
	base1="http://www.mirror.co.uk/all-about/"
	base2="?all=true"
	url=base1+slug+base2
	return url

 def mirror_parser(content,num):
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
		outstr=outstr
		fp=open("outputMirror.csv","a")
		fp.write(outstr)
	fp.close()"""
	
#	CODE TO CRAWL GOAL.COM	#

def goal_urlify(num):
	base="http://www.goal.com/en-gb/news/archive/"
	base+=str(num)
	return base
	
def goal_url_prefix(txt):
	base="http://www.goal.com"
	return base+txt

def goal_article_crawler(url):
	raw=crawl_page(url)
	parsed_url=BeautifulSoup(raw)
	out=["","",""]
	info=parsed_url.find("li",{"class":"tags"})
	if(len(info)==0):
		out[0]="Uncategorized"
	tags=""
	#print "TAGS INCOMING!!"
	for tag in info:
		#print tag.string.strip(',').strip('\n'),
		tags+=tag.string.strip(',').strip('\n')+"-"
	out[0]=tags
	time=parsed_url.find("time")['datetime']
	out[1]=time
	img=parsed_url.find("img",{"class":" article-image"})
	out[2]=img['src']
	
	return out
	
def goal_parser(content,num):
	count=0
	if(content==0):
		return
	parsed_url=BeautifulSoup(content)
	postsScraped=0
	all_posts=parsed_url.findAll("div",{"class":"articleInfo"})
	while (count<num):
		post=all_posts[count]
		#print post
		info=post.findAll("div", { "class" : None })
		info=info[1].find("a")
		#print info
		link=info['href']
		link=goal_url_prefix(link)
		title=info.contents[0]
		title=title.replace(',','')
		#print title[0:13]
		# SKIPPING TRANSFER TALK AND PLAYER RATINGS ARTICLES
		if(title[0:13]=="Transfer Talk"):
			count+=1
			continue
		if(title[0:14]=="Player Ratings"):
			count+=1
			continue
		blurb=post.find("div", { "class" : "articleSummary" }).contents[0]
		blurb=blurb.replace(',','')
		data=goal_article_crawler(link)
		img=str(data[2])
		data[0]=data[0]
		print "POST",count
		print "TITLE:",title
		print "BLURB:",blurb
		print "LINK:",link
		print "IMAGE:",img
		print "TIMESTAMP:",data[1]
		print "TAGS:",data[0]
		print "COUNT ",count,"POSTS ",postsScraped
		outstr=""
		outstr=title.encode("utf-8")+", "+blurb.encode("utf-8")+", "+link.encode("utf-8")+", "+img.encode("utf-8")+", "+data[0].encode("utf-8")+", "+data[1].encode("utf-8")+"\n"
		outstr=outstr
		fp=open("outputGoal.csv","a")
		fp.write(outstr)
		fp.close()
		count+=1
		postsScraped+=1
	if(postsScraped<num):
		goal_parser(crawl_page(goal_urlify(count/50+1)),num-postsScraped)
		
#name=raw_input("Enter the topic: ")
#num=int(raw_input("Enter the number of articles: "))
#name="Wayne Rooney"
num=35
guardian_parser(crawl_page("http://www.theguardian.com/football/all"),num)
#page=1
#mirror_parser(crawl_page(mirror_urlify(page)),num,page,0)
#goal_parser(crawl_page(goal_urlify(1)),num)
#str1="Southampton vs Burnley Live: English Barclays Premier League"
#str2="Live: English Barclays Premier League"
#print fuzz.partial_ratio(str1,str2)