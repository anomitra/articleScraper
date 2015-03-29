import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 
#import time
from BeautifulSoup import BeautifulSoup
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
#from time import sleep
import requests
from datetime import datetime

#Take this class for granted.Just use result of rendering.

start=datetime.now()
class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()
    self.frame.evaluateJavaScript("document.getElementById('statistics-table-summary')")
    self.app.quit()  

url = 'http://www.whoscored.com/Players/5583/#player-tournament-stats-summary'  
r = Render(url)  
result = r.frame.toHtml()
s=unicode(result)
s=s.encode("utf-8")
f=open("file1.html","w")
f.write(s)
f.close()
r=requests.get(url,timeout=10).text
r=r.encode("utf-8")
f=open("file2.html","w")
f.write(r)
f.close()
print "TIME TAKEN:",(datetime.now()-start).total_seconds()
