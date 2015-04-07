import requests
#import time
from BeautifulSoup import BeautifulSoup

def crawl_page(url):
	while True:
		try:
			#print "Trying to get URL... ",
			r=requests.get(url, timeout=5)
			#print "Got URL!"
			if(r.status_code==404):
				print "Sorry, but the page",url,"does not exist. Exiting."
				return 0
			return r.content
		except Exception as e:
			print e
			print "Retrying."
			
url="http://www.nba.com/teams/"
raw=crawl_page(url)
parsed_url=BeautifulSoup(raw)
rawnames=parsed_url.findAll("td",{"class":"nbateamname"})
for name in rawnames:
    new=name.find("a").contents[0]
    print new
    slug=name.find("a")['href']
    url="http://www.nba.com"+slug+"stats"
    print url
    raw=crawl_page(url)
    parsed=BeautifulSoup(raw)
    playernames=parsed.findAll("span",{"class":"playerName"})
    playerpics=parsed.findAll("img",{"width":"60px"})
    i=0
    f=open("test.html","w")
    f.write(str(parsed))
    f.close()
    for n in playernames:
        print n.find("a").contents[0]
        pic=playerpics[i]['src']
        print pic
        i+=1
        if(i==15):
            break
rawpics=parsed_url.findAll("img",{"class":"nbaImgPad"})
for pic in rawpics:
    new=pic['src']
    print new
