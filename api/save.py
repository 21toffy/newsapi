# from rest_framework.decorators import api_view
# from rest_framework import status
# from django.http import HttpResponseRedirect
# import mechanize
# from bs4 import BeautifulSoup
# from rest_framework.response import Response




# br = mechanize.Browser()
# br.set_handle_robots(False)
# br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
# from django.http import HttpResponse

# #Exceptions error 500 , 503 , Backend Error
# @api_view(['GET'])
# def vanguard (request, category):
#     vanguardlink="https://www.vanguardngr.com/category/{}/page/2".format(category)
#     # vanguardlink="https://www.vanguardngr.com/category/national-news/"
#     # https://www.vanguardngr.com/category/politics/
#     # https://www.vanguardngr.com/category/business/
#     # https://www.vanguardngr.com/category/health/
#     # https://www.vanguardngr.com/category/entertainment/
#     # https://www.vanguardngr.com/category/technology/
#     # https://www.vanguardngr.com/category/sports/
#     br.open(vanguardlink)
#     orders_html = br.response().read()

#     #initializing bs4 for scraping
#     soup = BeautifulSoup(orders_html,'html.parser')
#     # saves page source
#     orders_html = br.response().read()

#     #initializing bs4 for scraping
#     soup = BeautifulSoup(orders_html,'html.parser')

#     list_items = soup.find_all("article", {"class": "rtp-listing-post"})
#     titles=soup.find_all("h2", {"class": "entry-title"})

#     summaries=soup.find_all("div", {"class": "seg-summary"})
#     imagelinks = soup.find_all('a', {'class': 'rtp-thumb'})
#     dates=soup.find_all('time', {'class': 'entry-date'})

#     content=soup.find_all('div', {'class': 'entry-content'})
#     _id=[]
#     summary=[]
#     date=[]
#     vanguardphoto=[]
#     title=[]
#     link=[]
#     keys=['id','summary','date','photo','title', 'link']


#     for indtitle in titles:
#         varsingtitle=indtitle.find_all('a', href=True)
#         for therealink in varsingtitle:
#             link.append(therealink['href'])
#         shittitle=[]
#         for target in varsingtitle:
#             shittitle.append(target.find_all(text=True))
#             for singleshit in shittitle:
#                 for noshit in singleshit:
#                     title.append(noshit)

#     for identification in list_items:
#         _id.append(identification['id'])
#     # print(_id) 


#     for i in imagelinks:
#         d=i.find_all('img')
#         for i in d:
#             vanguardphoto.append(i['src'])


#     for timetravel in dates:
#         date.append(timetravel.find(text=True))

#     mad=[]
#     best=[]
#     for i in content:
#         mad.append(i.find_all(text=True))
#     for bingo in mad:
#         for local in bingo:
#             best.append(local)
#     for i in best:
#         if '\n' in i or "Read More" in i or i==" " :
#             del i
#         else:
#             summary.append(i)

        

#     data=[dict(zip(keys, i)) for i in zip(_id, summary, date, vanguardphoto, title, link)]
#     if len(data)==0:
#         print('the first gave 0', True)
#         data=[]
#         for i in range(len(keys)):
#                 data.append({'id':_id[i],'summary':summary[i],'date':date[i],'photo':vanguardphoto[i],'title':title[i],'link':link[i]})
#         print('second parameter was used', False)
#     else:
#         print('used the first', True)
     
#     return Response({"message": "Success!", "data": data}, status=status.HTTP_200_OK )