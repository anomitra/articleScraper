from pyvirtualdisplay import Display  
from selenium import webdriver 
from datetime import datetime, timedelta
from BeautifulSoup import BeautifulSoup
import re

def player_crawl(url,name):
    start=datetime.now()
    display = Display(visible=0, size=(800, 600))  
    display.start()  
    browser = webdriver.Firefox()  
    browser.get('http://www.whoscored.com/Players/5583/')  
    print "Time to get page for ",name," is ",datetime.now()-start
    print browser.title  
    stats=browser.find_element_by_id('statistics-table-summary')
    soup=BeautifulSoup(stats.get_attribute('innerHTML'))
    #soup=BeautifulSoup(stats.get_attribute('innerHTML'))
    #browser.quit()  
    #display.stop()
    f=open("whoScoredStats.csv","a")
    table=soup.find("tbody",{"id":"player-table-statistics-body"})
    rows=table.findAll("tr")
    for row in rows:
        fields=row.findAll("td")
        f.write(name.encode("utf-8")+", ")
        for field in fields:
            data=field.text
            if(data=="N/A" or data=="-"):
                data="0"
            data=re.sub('\([^)]*\)','', data)
            f.write(data.encode("utf-8")+", ")
        f.write("\n")
    print "Time to get stats for ",name," is ",datetime.now()-start
    f.close()

def team_page_crawler(num):
    url="http://www.whoscored.com/Teams/"+str(num)
    display = Display(visible=0, size=(800, 600))  
    display.start()  
    browser = webdriver.Firefox()  
    browser.get(url)  
    #print "TIME TO GET PAGE:",datetime.now()-start
    stats=browser.find_element_by_id('statistics-table-summary')
    soup=BeautifulSoup(stats.get_attribute('innerHTML'))
    table=soup.find("tbody",{"id":"player-table-statistics-body"})
    rows=table.findAll("tr")
    for row in rows:
        link=row.find("td",{"class":"pn"}).find("a",{"class":"player-link"})
        player_crawl(link['href'],link.text)

def stat_crawler(arr):
    for num in arr:
        team_page_crawler(num)

team_page_crawler(52)