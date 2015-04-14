import json
import urllib2
import urllib
from bs4 import BeautifulSoup

def request_ajax_data(url,data,referer=None,**headers):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116')
    if referer:
        req.add_header('Referer',referer)
    if headers:
        for k in headers.keys():
            req.add_header(k,headers[k])

    params = urllib.urlencode(data)
    response = urllib2.urlopen(req, params)
    jsonText = response.read()
    return jsonText
    #return json.loads(jsonText)

def get_prices(set_id):
    base_url = 'http://brickset.com'
    set_url = base_url+'/ajax/sets/buy'
    ajaxRequestBody = {"set":set_id}
#blogId,"postId":entryId,"blogApp":blogApp,"blogUserGuid":blogUserId}
    ajaxResponse = request_ajax_data(set_url, ajaxRequestBody)
    print ajaxResponse

def test():
    #set_id = '70161-1'
    #get_prices(set_id)

    with open('ajax.txt') as f:
        bs = BeautifulSoup(f.read())
        for tr in bs.find_all('tr')[1:]:
            tds = tr.find_all('td')
            current_price = tds[2].span.string
            retail_price = tds[3].string
            min_price = tds[4].contents[0]
            print current_price, retail_price, min_price
        """
        for span in bs.find_all('span', class_='disc'):
            print span
        for a in bs.find_all('a', class_='buynow'):
            print a['href']
        for td in bs.find_all('td'):
            print td.string
        """


if __name__ == '__main__':
    test()

