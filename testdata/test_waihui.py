from bs4 import BeautifulSoup

URL = 'http://fx.cmbchina.com/Hq/'

with open('test_waihui.html') as f:
    bs = BeautifulSoup(f.read())
    for tr in bs.select("#realRateInfo")[0].find_all("tr"):
        print [td.text.strip() for td in tr.find_all("td")]

