from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpResponseRedirect
import mechanize
from bs4 import BeautifulSoup
from rest_framework.response import Response
from collections import Counter
from users.models import Profile 

import random




br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br2 = mechanize.Browser()
br2.set_handle_robots(False)
br2.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]




@api_view(['GET'])
def search(request, searchterm, apikey):
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

        br.open("https://punchng.com/search/{}".format(searchterm))

        br2.open("https://punchng.com/search/{}/page/2/".format(searchterm))

        # saves page source
        orders_html = br.response().read()

        orders_html2 = br2.response().read()
        #initializing bs4 for scraping
        soup = BeautifulSoup(orders_html,'html.parser')
        # saves page source

        #initializing bs4 for scraping
        soup2 = BeautifulSoup(orders_html2,'html.parser')

        list_items = soup.find_all("div", {"class": "items"})
        titles=soup.find_all("h2", {"class": "seg-title"})
        summaries=soup.find_all("div", {"class": "seg-summary"})
        dates=soup.find_all("div", {"class": "seg-time"})
        imagelinks = soup.find_all('figure', {'class': 'seg-image'})



        list_items2 = soup2.find_all("div", {"class": "items"})
        titles2=soup2.find_all("h2", {"class": "seg-title"})
        summaries2=soup2.find_all("div", {"class": "seg-summary"})
        dates2=soup2.find_all("div", {"class": "seg-time"})
        imagelinks2 = soup2.find_all('figure', {'class': 'seg-image'})



        link=[]
        title=[]
        summary=[]
        date=[]
        largeimage=[]
        _id=[]
        keys=['id','summary','date','photo','title', 'link']



        link2=[]
        title2=[]
        summary2=[]
        date2=[]
        largeimage2=[]
        _id2=[]


        for tit in titles:
            title.append(tit.find(text=True))


        for tit in titles2:
            title2.append(tit.find(text=True))


        for sum in summaries:
            randoms = sum.find_all('p')
            for realshit in randoms:
                summary.append(realshit.find(text=True))

        
        for sum in summaries2:
            randoms2 = sum.find_all('p')
            for realshit in randoms2:
                summary2.append(realshit.find(text=True))



        for data in dates:
            fin=data(text=True)

            for i in fin:
                date.append(i.replace('\n',' '))
        
        for data in dates2:
            fin2=data(text=True)

            for i in fin2:
                date2.append(i.replace('\n',' '))


        for i in title:
            _id.append(title.index(i))

        for i in title2:
            xxx=random.randint(1,1000)
            _id2.append(title2.index(i)+xxx)


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

        data1=[dict(zip(keys, i)) for i in zip(_id, summary, date, largeimage, title, link)]
        data2=[dict(zip(keys, i)) for i in zip(_id2, summary2, date2, largeimage2, title2, link2)]
        data=data1+data2
        if len(data)==0:
            print('using this')
            
            data1=[]
            
            for i in range(len(keys)):
                data1.append({'id':_id[i],'summary':summary[i],'date':date[i],'photo':largeimage[i],'title':title[i],'link':link[i]})
            data2=[]
            for i in range(len(keys)):
            
                data2.append({'id':_id2[i],'summary':summary2[i],'date':date2[i],'photo':largeimage2[i],'title':title2[i],'link':link2[i]})
            data=data1+data2
            return Response ({"message": "Success!", "data": data}, status=status.HTTP_200_OK )
        return Response({"message": "Success!", "data": data}, status=status.HTTP_200_OK )

    except Exception as e:
        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back)
        return Response({"message": "somekind of error! try again", "data": message}, status=status.HTTP_503_SERVICE_UNAVAILABLE )