from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework import status
from django.http import HttpResponseRedirect
import mechanize
from bs4 import BeautifulSoup
from rest_framework.response import Response
from collections import Counter
from users.permissions import OnlyAPIPermission
import random
from django.contrib.auth.models import User as User
from users.models import Profile 
from django.http import Http404
from datetime import timezone, timedelta, datetime
from rest_framework.throttling import UserRateThrottle
 
import traceback
import sys

from users.models import Profile 




br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br2 = mechanize.Browser()
br2.set_handle_robots(False)
br2.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


@api_view(['GET'])
def punch (request, category, apikey):
    cate=["politics", 'business','news','entertainment', 'technology','sports'] 
    if category not in cate:
        data="invalid category entered in the query string parameter. fix or Read the docs"
        return Response ({"message": data}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        user_Key = Profile.objects.get(api_key=apikey)
    except Profile.DoesNotExist:
        data= "Your Api Key or username is Invalid. carefully check and fix!"
        return Response ({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            
    currentuser = Profile.objects.get(api_key=apikey)
    if currentuser.no_of_requests>=1000:
        return Response ({"message": "you have exhausted all your requests for the day"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    currentuser.no_of_requests=currentuser.no_of_requests + 1
    currentuser.save()
    try:
        
        kind="https://punchng.com/topics/{}/".format(category)
        kind2 = "https://punchng.com/topics/{}/page/2".format(category)
        br.open(kind)
        br2.open(kind2)
        # br.open("https://punchng.com/topics/news/")
        # https://punchng.com/topics/entertainment/
        # br.open("https://punchng.com/topics/business/")
        # br.open("https://punchng.com/topics/sports/")
        # https://punchng.com/topics/technology/

        # br.open("https://punchng.com/topics/politics/page/2")
        # br.open("https://punchng.com/topics/news/page/2")
        # br.open("https://punchng.com/topics/business/page/2")
        # br.open("https://punchng.com/topics/sports/page/2")

        # br.open("https://punchng.com/search/coronavirus")



            


        # saves page source
        orders_html = br.response().read()

        # saves page source
        orders_html2 = br2.response().read()

        #initializing bs4 for scraping
        soup = BeautifulSoup(orders_html,'html.parser')
        print(soup)
        #initializing bs4 for scraping
        soup2 = BeautifulSoup(orders_html2,'html.parser')


        #got the div wrapping each listed news element
        list_items = soup.find_all("div", {"class": "items"})

        #got the div wrapping each listed news element
        list_items2 = soup2.find_all("div", {"class": "items"})

        #got the h2 tag wrapping each listed title 
        titles=soup.find_all("h2", {"class": "seg-title"})
            #got the h2 tag wrapping each listed title 
        titles2=soup2.find_all("h2", {"class": "seg-title"})

        summaries=soup.find_all("div", {"class": "seg-summary"})
        summaries2=soup2.find_all("div", {"class": "seg-summary"})

        dates=soup.find_all("div", {"class": "seg-time"})
        dates2=soup2.find_all("div", {"class": "seg-time"})


        imagelinks = soup.find_all('figure', {'class': 'seg-image'})
        imagelinks2 = soup2.find_all('figure', {'class': 'seg-image'})
        print(imagelinks)
        print(imagelinks2)




        link=[]
        title=[]
        summary=[]
        date=[]
        largeimage=[]
        _id=[]

        link2=[]
        title2=[]
        summary2=[]
        date2=[]
        largeimage2=[]
        _id2=[]
        #keys for the to create a dictionary
        keys=['id','summary','date','photo','title', 'link']

        

        #looping to append titles to the list
        for tit in titles:
            title.append(tit.find(text=True))

        

        #looping to append titles to the list
        for tit in titles2:
            title2.append(tit.find(text=True))

        # looping to make the index of each element represented by the title be the id of that news element
        for i in title:
            _id.append(title.index(i))

        
        # looping to make the index of each element represented by the title be the id of that news element
        for i in title2:
            xxx=random.randint(1,1000)
            _id2.append(title2.index(i)+xxx)


        # appending summary to list
        for sum in summaries:
            randoms = sum.find_all('p')
            for realshit in randoms:
                summary.append(realshit.find(text=True))



        # appending summary to list
        for sum in summaries2:
            random2 = sum.find_all('p')
            for realshit in random2:
                summary2.append(realshit.find(text=True))


        for data in dates:
            randomed = data.find_all('span')
            for realshit in randomed:
                date.append(realshit.find(text=True))


        for data in dates2:
            random2 = data.find_all('span')
            for realshit in random2:
                date2.append(realshit.find(text=True))


        # for sfoto in imagelinks:
        #     smallimage.append(sfoto['data-src-small'])

        for pfoto in imagelinks:
            largeimage.append(pfoto['data-src'])
            
        for pfoto in imagelinks2:
            largeimage2.append(pfoto['data-src'])

        

        for insecure in list_items:
            links = insecure.find_all('a', href=True)
            for hyper in links:
                link.append(hyper['href'])

        for insecure in list_items2:
            links2 = insecure.find_all('a', href=True)
            for hyper in links2:
                link2.append(hyper['href'])


        print(link2)


        data1=[dict(zip(keys, i)) for i in zip(_id, summary, date, largeimage, title, link)]
        data2=[dict(zip(keys, i)) for i in zip(_id2, summary2, date2, largeimage2, title2, link2)]
        data=data1+data2
        print(len(data), "..........................--------------------")
        if len(data)==0:
            
            data1=[]
            
            for i in range(len(keys)):
                    data1.append({'id':_id[i],'summary':summary[i],'date':date[i],'photo':largeimage[i],'title':title[i],'link':link[i]})
            data2=[]
            for i in range(len(keys)):
                    data2.append({'id':_id2[i],'summary':summary2[i],'date':date2[i],'photo':largeimage2[i],'title':title2[i],'link':link2[i]})
            data=data1+data2
            print("this went well")
            return Response ({"message": "Success!", "data": data}, status=status.HTTP_200_OK )
        return Response ({"message": "Success!", "data": data}, status=status.HTTP_200_OK )
    except Exception as e:
        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back)
        return Response({"message": "somekind of error! try again", "data": message}, status=status.HTTP_503_SERVICE_UNAVAILABLE )
    
    