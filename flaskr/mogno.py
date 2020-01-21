# import requests as req
# from bs4 import BeautifulSoup as soup
from pymongo import MongoClient
from pymongo import InsertOne
# from hashlib import md5
# import re
# from multiprocessing.dummy import Pool  # This is a thread-based Pool
# from multiprocessing import cpu_count

client = MongoClient('localhost',27017)
#print(client.list_database_names())

mydb = client["darkboard"]
mycoll=mydb["local-services"]
mycoll_1 = mydb["categories"]


unscrapped_urls = []
operations = []

# gets all the urls of the sections present in the url given
def GetAllLinks(url):
    resp = req.get(url)
    p = soup(resp.text, 'html.parser')
    cont = p.select(".row")
    #print(len(cont))

    links = []
    if(cont is not None):
        for link in cont[0].findAll("a",href=True):
            #print(link.get('href'))
            links.append("https://www.sulekha.com" + link.get('href'))
        return links

# to scrape all the pages of a section, we need the hidden url of the first page of the particular
# section. This function gets all those hidden urls. This hidden url is given as a parameter for
# the ScrapeAllPages function.
def GetHiddenUrls(links):
    urls = []
    for link in links:
        resp_1 = req.get(link)
        p_1 = soup(resp_1.text, 'html.parser')
        if(p_1.select("input[id^=partialPageData]")):
            cont = p_1.select("input[id^=partialPageData]")
            partialPageData = str(cont[0]).split("value=")[1].strip("/>")
            partialPageData = re.sub('["]','',partialPageData)
        else:
            unscrapped_urls.append(link)
            continue
        if(p_1.select("input[id^=hdnCategoryName]")):
            cont_1 = p_1.select("input[id^=hdnCategoryName]")
            categoryName = str(cont_1[0]).split("value=")[1].strip("/>")
            categoryName = re.sub('["]','',categoryName)
        #categoryName = categoryName.strip('"')
        if(p_1.select("input[id^=hdnCategoryId]")):
            cont_1 = p_1.select("input[id^=hdnCategoryId]")
            categoryId = str(cont_1[0]).split("value=")[1].strip("/>")
            categoryId = re.sub('["]','',categoryId)
        if(p_1.select("input[id^=hdnCityName]")):
            cont_1 = p_1.select("input[id^=hdnCityName]")
            cityName = str(cont_1[0]).split("value=")[1].strip("/>")
            cityName = re.sub('["]','',cityName)
        url = "https://www.sulekha.com/mvc5/lazy/v1/Listing/get-business-list?PartialPageData=" + partialPageData + "&Category=" + categoryId + "&Filter=%7B%7D&PageNr=1&Sort=&getQuoteVisiblity=&aboutEnabled=&CategoryName=" + categoryName + "&CityName=" + cityName + "&IsAboutEnabled=True&fp=0&tp=0&fa=0&ta=0&au="
        #print(url)
        urls.append(url)

    return urls


'''
filename = "retail.csv"
f = open(filename,'w')
headers = "Shop_Name,Type,City,Area,Address\n"
f.write(headers)'''	

#myList = []

#after the last page got scrapped, the next page will be empty. Then this function will return zero.
def LengthOfContainers(url):
    resp = req.get(url)
    p = soup(resp.text, 'html.parser')
    containers = p.select(".wraper")
    return len(containers)

#scrapes the current page of the given url (hidden url)
#hidden url looks something like this
'''https://www.sulekha.com/mvc5/lazy/v1/Listing/get-business-list?PartialPageDat
a=eyIkaWQiOiIxIiwiQ2l0eUlkIjozLCJBcmVhSWQiOjAsIkNhdGVnb3J5SWQiOjE1LCJOZWVkSWQiOj
AsIk5lZWRGaWx0ZXJWYWx1ZXMiOiIxOTA3MDA6NjE2MzAwIiwiUm91dGVOYW1lIjoiQ29ycG9yYXRlI
Exhd3llcnMiLCJQYWdlVmlld1R5cGUiOjQsIkhhc0xjZiI6dHJ1ZSwiQnJlYWRDcnVtYlRpdGxlIjoi
Q29ycG9yYXRlIExhd3llcnMiLCJJc09ubHlQcmltYXJ5VGFnIjp0cnVlLCJDbGVhckNhY2hlIjpmYWx
zZSwiSHViSWQiOiIiLCJBdHRyaWJ1dGVzIjoiMTkwNzAwOjYxNjMwMCIsIlZlcnNpb24iOjIsIklzQ
WRMaXN0aW5nUGFnZSI6ZmFsc2UsIklzQWREZXRhaWxQYWdlIjpmYWxzZSwiUmVmTmVlZElkIjowLCJ
UZW1wbGF0ZU5hbWUiOiIiLCJJc1B3YSI6ZmFsc2UsIkRpc2FibGVHb29nbGVBZHMiOmZhbHNlLCJTd
GF0ZUNvZGUiOiJBUCJ9&Category=15&Filter=%7B%22NeedFilterValues%22%3A%7B
%22190700%22%3A%5B%22616300%22%5D%7D%7D&PageNr=1&Sort=&getQuoteVisiblity=
&aboutEnabled=&CategoryName=Advocates+%26+Lawyers&CityName=Hyderabad
&IsAboutEnabled=False&fp=0&tp=0&fa=0&ta=0&au='''
def ScrapeCurrentPage(url):
    resp = req.get(url)
    p = soup(resp.text, 'html.parser')
    containers = p.select(".wraper")
    #city = "Banglore"
    city_split = url.split("CityName=")
    city = city_split[1]
    city_spl = city.split("&")
    city = city_spl[0]
    source = md5(url.encode("utf-8")).hexdigest()

    if(mycoll.find_one({"Source" : str(source)}) == None):
        for cont in containers:
            shop_name = cont.a.h3.text
            shop_name = shop_name.replace(","," ")
            link = "https://www.sulekha.com" + cont.find("a",href=True).get('href')
            #city = "Hyderabad"
            location = cont.find("span",{"class":"location"}).text
            loc_split = location.split(",")
            area = loc_split[-1].strip()
            if(cont.find("p",{"class":"icon-tag f-icon"})):
                service = cont.find("p",{"class":"icon-tag f-icon"}).text
            else:
                service = "NA"
            if(cont.find("b",{"class":"icon-phone f-icon isbvn"})):
                mobile = cont.find("b",{"class":"icon-phone f-icon isbvn"}).text
            else:
                mobile = "NA"
            #mobile = cont.find("b",{"class":"icon-phone f-icon isbvn"}).text
            if(cont.find("address",{"class":"icon-address f-icon"})):
                address = cont.find("address",{"class":"icon-address f-icon"}).text
                address = address.replace(","," ")
                address = address.strip("Get Directions")
            else:
                address = location

            resp_1 = req.get(link)
            p_1 = soup(resp_1.text, 'html.parser')
            containers_2 = p_1.select("div[id^=contacts]")

            if(containers_2[0].find("div",{"class":"person"})):
                name = containers_2[0].find("div",{"class":"person"}).text
                name_split = name.split("Person")
                name = name_split[1].strip()
                name = name.replace(","," ")
            else:
                name = "NA"

            if(containers_2[0].find("div",{"class":"hours"})):
                working = containers_2[0].find("div",{"class":"hours"}).text
                working = working.strip("Working Hours")
            else:
                working = "NA"

            #operations.append(InsertOne({"Shop_Name": shop_name, "Owner_Name": name, "Type_of_Shop": service, "City": city, "Area": area, "Address": address, "Contact": mobile, "Working_Hours": working, "Source": source}))
            mycoll.insert_one({"Shop_Name": shop_name, "Owner_Name": name, "Type_of_Shop": service, "City": city, "Area": area, "Address": address, "Contact": mobile, "Working_Hours": working, "Source": source})
            #myList.append({"Shop_Name": shop_name, "Owner_Name": name, "Type_of_Shop": service, "City": city, "Area": area, "Address": address, "Working_Hours": working, "Source": source})

            print(shop_name + "..." + name + "..." + service + "..." +  city + "..." + area + "..." + address + "..." + mobile + "..." + working + "..." + source)
            print("\n")
            #f.write(shop_name + "," + service + "," +  city + "," + area + "," + address + "\n")

        #f.write(firm_name + "," + name + "," + services + "," + city + "," + area + "," + mobile + "," + address + "," + email + "\n")

#scrapes all the pages when the url to the first page is given
def ScrapeAllPages(url):
    #ScrapeCurrentPage(url)
    page = 1
    while(LengthOfContainers(url)>0):
        print(page)
        original_page = "PageNr=" + str(page)
        replace_page = "PageNr=" + str(page+1)
        ScrapeCurrentPage(url)
        url = url.replace(original_page,replace_page)
        page += 1

#scrapes all the pages of sulekha website corresponding to the given city
#city name must be given as a string
def ScrapeByCity(city):
    url = "https://www.sulekha.com/local-services/" + city
    links = GetAllLinks(url)
    hidden_urls = GetHiddenUrls(links)
    for hdnUrl in hidden_urls:
    	ScrapeAllPages(hdnUrl)

#scrapes all the pages corresponding to the url given
# for example: Scrape("https://www.sulekha.com/atms/hyderabad") gets
# all the data of atms in hyderabad
def Scrape(url):
    links = []
    links.append(url)
    hidden_urls = GetHiddenUrls(links)
    for hdnUrl in hidden_urls:
    	ScrapeAllPages(hdnUrl)
    	#mycoll.bulk_write(operations)
    city = url.split("/")
    print(city[-2] + " of " + city[-1] + " is completed.\n")

# we will give link of the particular category,
# like https://www.sulekha.com/atms , and this function tells us whether
# all the elements of that category are scrapped
def IsCategoryScrapped(link):
    if(mycoll_1.find_one({"$and" : [{"url":link},{"Status":"Done"}]}) == None):
        return False
    else:
        return True

def MultithreadScraper(url):
    thread_factor = 10
    pool = Pool(cpu_count() * thread_factor)
    categories = GetAllLinks(url)
    for link in categories:
        if(IsCategoryScrapped(link)==False):
            url = link + "all-cities"
            cities = GetAllLinks(url)
            pool.map(Scrape,cities)
            print("Category: " + url.split("/")[-2] + " is completed.\n")
            mycoll_1.insert_one({"url":link, "Status":"Done"})
        else:
            continue
    pool.close()
    pool.join()

#gets all the cities supported by sulekha (around 1700 cities were there)
'''def ListAllCities(url):
    resp = req.get(url)
    p = soup(resp.text, 'html.parser')
    cont = p.select(".unstyled")
    cities = []
    for i in cont:
        for j in i.find_all('a'):
            cities.append(j.text.replace(" ",""))
    return cities'''

def main():
    #url = "https://www.sulekha.com/mvc5/lazy/v1/Listing/get-business-list?PartialPageData=eyIkaWQiOiIxIiwiQ2l0eUlkIjozLCJBcmVhSWQiOjAsIkNhdGVnb3J5SWQiOjE1LCJOZWVkSWQiOjAsIk5lZWRGaWx0ZXJWYWx1ZXMiOiIxOTA3MDA6NjE2MzAwIiwiUm91dGVOYW1lIjoiQ29ycG9yYXRlIExhd3llcnMiLCJQYWdlVmlld1R5cGUiOjQsIkhhc0xjZiI6dHJ1ZSwiQnJlYWRDcnVtYlRpdGxlIjoiQ29ycG9yYXRlIExhd3llcnMiLCJJc09ubHlQcmltYXJ5VGFnIjp0cnVlLCJDbGVhckNhY2hlIjpmYWxzZSwiSHViSWQiOiIiLCJBdHRyaWJ1dGVzIjoiMTkwNzAwOjYxNjMwMCIsIlZlcnNpb24iOjIsIklzQWRMaXN0aW5nUGFnZSI6ZmFsc2UsIklzQWREZXRhaWxQYWdlIjpmYWxzZSwiUmVmTmVlZElkIjowLCJUZW1wbGF0ZU5hbWUiOiIiLCJJc1B3YSI6ZmFsc2UsIkRpc2FibGVHb29nbGVBZHMiOmZhbHNlLCJTdGF0ZUNvZGUiOiJBUCJ9&Category=15&Filter=%7B%22NeedFilterValues%22%3A%7B%22190700%22%3A%5B%22616300%22%5D%7D%7D&PageNr=1&Sort=&getQuoteVisiblity=&aboutEnabled=&CategoryName=Advocates+%26+Lawyers&CityName=Hyderabad&IsAboutEnabled=False&fp=0&tp=0&fa=0&ta=0&au="
    #ScrapeAllPages(url)
    #url_1 = "https://www.sulekha.com/mvc5/lazy/v1/Listing/get-business-list?PartialPageData=eyIkaWQiOiIxIiwiQ2l0eUlkIjo1LCJBcmVhSWQiOjAsIkNhdGVnb3J5SWQiOjE1LCJOZWVkSWQiOjAsIk5lZWRGaWx0ZXJWYWx1ZXMiOiIxOTA3MDA6NjE2MzAwIiwiUm91dGVOYW1lIjoiQ29ycG9yYXRlIExhd3llcnMiLCJQYWdlVmlld1R5cGUiOjQsIkhhc0xjZiI6dHJ1ZSwiQnJlYWRDcnVtYlRpdGxlIjoiQ29ycG9yYXRlIExhd3llcnMiLCJJc09ubHlQcmltYXJ5VGFnIjp0cnVlLCJDbGVhckNhY2hlIjpmYWxzZSwiSHViSWQiOiIiLCJBdHRyaWJ1dGVzIjoiMTkwNzAwOjYxNjMwMCIsIlZlcnNpb24iOjIsIklzQWRMaXN0aW5nUGFnZSI6ZmFsc2UsIklzQWREZXRhaWxQYWdlIjpmYWxzZSwiUmVmTmVlZElkIjowLCJUZW1wbGF0ZU5hbWUiOiIiLCJJc1B3YSI6ZmFsc2UsIkRpc2FibGVHb29nbGVBZHMiOmZhbHNlLCJTdGF0ZUNvZGUiOiJETCJ9&Category=15&Filter=%7B%22NeedFilterValues%22%3A%7B%22190700%22%3A%5B%22616300%22%5D%7D%7D&PageNr=1&Sort=&getQuoteVisiblity=&aboutEnabled=&CategoryName=Advocates+%26+Lawyers&CityName=Delhi&IsAboutEnabled=False&fp=0&tp=0&fa=0&ta=0&au="
    #ScrapeAllPages(url_1)
    url = "https://www.sulekha.com/local-services/"
    #url = "https://www.sulekha.com/gynecologists-obstetricians/all-cities"

    # gets links to all the categories listed in the url
    # that is categories have links like "https://www.sulekha.com/atms/" and so on
    #categories = GetAllLinks(url)
    #for cat in categories:
     #   print(cat)
    #cities = ListAllCities(url)

    # for each category we will get links to all the cities that category shops were present
    # that is, lets say, for atms, we will get links that have the data of all the atms present in that city, like
    # "https://www.sulekha.com/atms/bangalore", "https://www.sulekha.com/atms/hyderabad" and so on
    # this is done like this because every category will have different number of cities. for atms, we have 1366 cities
    # for banks we have 1344 cities and so on.
    '''for link in categories:
        link = link + "all-cities"
        cities = GetAllLinks(link)
        pool.map(Scrape,cities)
        #for city in cities:
         #   Scrape(city)
        #pool.close()
        #pool.join()
        #cities.clear()
        print("Category: " + link.split("/")[-2] + " is completed.\n")'''

    MultithreadScraper(url)

    #cities = ["Srikakulam","Rajam"]
    #pool.map(ScrapeByCity,cities)
    #pool.close()
    #pool.join()

    for url in unscrapped_urls:
        print(url)
    #ScrapeByCity("Hyderabad")
    #ScrapeByCity("Chennai")
    '''filename = "sites_1.txt"
    f = open(filename, 'r')
    #print(f.readline())
    urls = []
    for x in f:
        y = x.split(",")

    for i in y:
        urls.append(i)

    for url in urls:
        ScrapeAllPages(url)'''

    #x = mycoll.insert_many(myList)


if __name__ == "__main__":
    main()

#f.close()
