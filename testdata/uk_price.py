from bs4 import BeautifulSoup
from urllib import urlopen


base_url = 'http://brickset.com'
buy_uk_url = '/buy/vendor-amazon/country-uk/order-percentdiscount/page-1'
text = urlopen(base_url + buy_uk_url).read()
soup = BeautifulSoup(text)
divs = soup.find_all('div', class_='tags hideonmediumscreen')
for div in divs:
    set_url = base_url + div.a['href']

