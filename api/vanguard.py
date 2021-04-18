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


br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]



br2 = mechanize.Browser()
br2.set_handle_robots(False)
br2.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


# @throttle_classes([UserRateThrottle])
from django.http import HttpResponse


@api_view(['GET'])
# @renderer_classes([JSONRenderer])
def vanguard (request, category, apikey):
    cate=["politics", 'business','health', 'entertainment', 'technology','sports'] 
    if category not in cate:
        data="invalid category entered in the query string parameter. fix or Read the docs"
        return Response ({"message": data}, status=status.HTTP_400_BAD_REQUEST)  
    try:
        user_Key = Profile.objects.get(api_key=apikey)
    except Profile.DoesNotExist:
        data= "Your Api Key is bad. carefully check and fix!. or go to https:9janewsapi.herokuapp.com to get one"
        return Response ({"message": data}, status=status.HTTP_400_BAD_REQUEST)
            
    currentuser = Profile.objects.get(user=request.user)
    print(currentuser)
    if currentuser.no_of_requests>=50:
        return Response ({"message": "you have exhausted all your requests for the day"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    currentuser.no_of_requests=currentuser.no_of_requests + 1
    currentuser.save()
    try:
        vanguardlink="https://www.vanguardngr.com/category/{}/".format(category)
        vanguardlink2="https://www.vanguardngr.com/category/{}/page/2".format(category)

        br.open(vanguardlink)
        br2.open(vanguardlink2)
        orders_html = br.response().read()
        orders_html2 = br2.response().read()

        #initializing bs4 for scraping
        soup = BeautifulSoup(orders_html,'html.parser')
        soup2 = BeautifulSoup(orders_html2,'html.parser')

        # saves page source
        orders_html = br.response().read()
        orders_html2 = br.response().read()

        #initializing bs4 for scraping
        soup = BeautifulSoup(orders_html,'html.parser')
        soup2 = BeautifulSoup(orders_html2,'html.parser')

        list_items = soup.find_all("article", {"class": "rtp-listing-post"})
        list_items2 = soup2.find_all("article", {"class": "rtp-listing-post"})

        titles=soup.find_all("h2", {"class": "entry-title"})
        titles2=soup2.find_all("h2", {"class": "entry-title"})

        summaries=soup.find_all("div", {"class": "seg-summary"})
        summaries2=soup2.find_all("div", {"class": "seg-summary"})

        imagelinks = soup.find_all('a', {'class': 'rtp-thumb'})
        imagelinks2 = soup2.find_all('a', {'class': 'rtp-thumb'})

        dates=soup.find_all('time', {'class': 'entry-date'})
        dates2=soup2.find_all('time', {'class': 'entry-date'})

        content=soup.find_all('div', {'class': 'entry-content'})
        content2=soup2.find_all('div', {'class': 'entry-content'})

        _id=[]
        summary=[]
        date=[]
        vanguardphoto=[]
        title=[]
        link=[]
        keys=['id','summary','date','photo','title', 'link']

        
        _id2=[]
        summary2=[]
        date2=[]
        vanguardphoto2=[]
        title2=[]
        link2=[]


        for indtitle in titles:
            varsingtitle=indtitle.find_all('a', href=True)
            for therealink in varsingtitle:
                link.append(therealink['href'])
            shittitle=[]
            for target in varsingtitle:
                shittitle.append(target.find_all(text=True))
                for singleshit in shittitle:
                    for noshit in singleshit:
                        title.append(noshit)

        for indtitle in titles2:
            varsingtitle=indtitle.find_all('a', href=True)
            for therealink in varsingtitle:
                link2.append(therealink['href'])
            shittitle=[]
            for target in varsingtitle:
                shittitle.append(target.find_all(text=True))
                for singleshit in shittitle:
                    for noshit in singleshit:
                        title2.append(noshit)
        
        titlelength=len(title)
        for identification in list_items:
            _id.append(identification['id'])
        if len(_id)==0:
            for i in range(titlelength):
                xxx=random.randint(1,1000)
                _id.append(xxx)


        for identification in list_items2:
            _id2.append(identification['id'])
        if len(_id2)==0:
            for i in range(titlelength):
                xxx=random.randint(1,1000)
                _id2.append(xxx)
                    


        for i in imagelinks:
            d=i.find_all('img')
            for i in d:
                vanguardphoto.append(i['src'])
        if len(vanguardphoto)==0:
            for i in range(titlelength):
                xxx='null'
                vanguardphoto.append(xxx)



        for timetravel in dates:
            date.append(timetravel.find(text=True))

        
        for i in imagelinks2:
            d=i.find_all('img')
            for i in d:
                vanguardphoto2.append(i['src'])
        if len(vanguardphoto2)==0:
            for i in range(titlelength):
                xxx='null'
                vanguardphoto2.append(xxx)


        for timetravel in dates2:
            date2.append(timetravel.find(text=True))

        mad=[]
        best=[]
        for i in content:
            mad.append(i.find_all(text=True))
        for bingo in mad:
            for local in bingo:
                best.append(local)
        for i in best:
            if '\n' in i or "Read More" in i or i==" " :
                del i
            else:
                summary.append(i)


        mad2=[]
        best2=[]
        for i in content2:
            mad2.append(i.find_all(text=True))
        for bingo in mad2:
            for local in bingo:
                best2.append(local)
        for i in best2:
            if '\n' in i or "Read More" in i or i==" " :
                del i
            else:
                summary2.append(i)
        
    

        data1=[dict(zip(keys, i)) for i in zip(_id, summary, date, vanguardphoto, title, link)]
        data2=[dict(zip(keys, i)) for i in zip(_id2, summary2, date2, vanguardphoto2, title2, link2)]

        data=data1+data2  
        fam=[]
        if len(data)==0:
            
            data1=[]
    
            
            for i in range(len(keys)):
                    data1.append({'id':_id[i],'summary':summary[i],'date':date[i],'photo':vanguardphoto[i],'title':title[i],'link':link[i]})
            data2=[]
            for i in range(len(keys)):
                    data2.append({'id':_id2[i],'summary':summary2[i],'date':date2[i],'photo':vanguardphoto2[i],'title':title2[i],'link':link2[i]})
            data=data1+data2        
            return Response ({"message": "Success!", "data": data}, status=status.HTTP_200_OK )
        return Response({"message": "Success!", "data": data}, status=status.HTTP_200_OK )
    except Exception as e:
        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back)
        return Response({"message": "somekind of error! try again", "data": message}, status=status.HTTP_503_SERVICE_UNAVAILABLE )






