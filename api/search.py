from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpResponseRedirect
import mechanize
from bs4 import BeautifulSoup
from rest_framework.response import Response
from collections import Counter

import random




br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]




@api_view(['GET'])
def search(request, searchterm):

    br.open("https://punchng.com/search/{}".format(searchterm))

    # saves page source
    orders_html = br.response().read()

    #initializing bs4 for scraping
    soup = BeautifulSoup(orders_html,'html.parser')
    # saves page source
    orders_html = br.response().read()

    #initializing bs4 for scraping
    soup = BeautifulSoup(orders_html,'html.parser')

    list_items = soup.find_all("div", {"class": "items"})
    titles=soup.find_all("h2", {"class": "seg-title"})
    summaries=soup.find_all("div", {"class": "seg-summary"})
    dates=soup.find_all("div", {"class": "seg-time"})
    imagelinks = soup.find_all('figure', {'class': 'seg-image'})



    link=[]
    title=[]
    summary=[]
    date=[]
    largeimage=[]
    _id=[]
    keys=['id','summary','date','photo','title', 'link']


    for tit in titles:
        title.append(tit.find(text=True))

    for sum in summaries:
        random = sum.find_all('p')
        for realshit in random:
            summary.append(realshit.find(text=True))



    for data in dates:
        fin=data(text=True)

        for i in fin:
            date.append(i.replace('\n',' '))


    for i in title:
        _id.append(title.index(i))


    for pfoto in imagelinks:
        largeimage.append(pfoto['data-src'])

    for insecure in list_items:
        links = insecure.find_all('a', href=True)
        for hyper in links:
            link.append(hyper['href'])

    data=[dict(zip(keys, i)) for i in zip(_id, summary, date, largeimage, title, link)]
    if len(data)==0:
        
        data=[]
        
        for i in range(len(keys)):
            data.append({'id':_id[i],'summary':summary[i],'date':date[i],'photo':largeimage[i],'title':title[i],'link':link[i]})
        return Response ({"message": "Success!", "data": data}, status=status.HTTP_200_OK )
    return Response({"message": "Success!", "data": data}, status=status.HTTP_200_OK )
