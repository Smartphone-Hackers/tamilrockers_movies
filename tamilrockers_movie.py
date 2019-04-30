import requests
import os
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://eu0.proxysite.com/includes/process.php?action=update"

proxysite = "https://eu0.proxysite.com"
 
form = {
    'server-option':'eu0',
    'd':'tamilrockers.com',
    'allowCookies':'on'
}

tamilrockers = requests.post(url=url,data=form).text

name = re.findall(r'http://tamil[a-z0-9]+\.[a-z]{2,3}',tamilrockers)
tamilrockers_domain_name = name[0]

print('*'*40)
print('Domain Name : {}'.format(tamilrockers_domain_name))
print('*'*40)

movies_name_lists = []
movie_ids = []

form = {
    'd':'{}/index.php/forum/115-tamil-new-dvdrips-hdrips-bdrips-movies/'.format(tamilrockers_domain_name),
    'allowCookies':'on'
}

more_movies = requests.post(url=url, data=form).content

soup = BeautifulSoup(more_movies,'lxml')

div_tag = soup.find_all('div',{"class":"ipsBox_container"})

for div in div_tag:
    a_tag = div.find_all("a",{"class":"topic_title"})

    for a in a_tag:
        movies_name_lists.append(a.find('span',{"itemprop":"name"}).text)

movie_full_title = []
movie_half_url = []

for div in div_tag:

    title_gen = div.find_all('span',{"itemprop":"name"})

    for title in title_gen:
        t = title.text
        k = ''.join(re.findall(r'[^\(\)\[\]-]',t))
        movie_full_title.append(k.replace('  ',' ').replace('.','').replace(' ','-').lower())

    a_tag = div.find_all('a') 

    for a in a_tag:
        movie_id = a.get('id')
                    
        if movie_id != None:           
            id_gen = movie_id.split('-')[-1]
            
            if id_gen.isdigit():

                movie_half_url.append(tamilrockers_domain_name+'/index.php/topic/'+id_gen)

movie_name_and_url = {}

print('Movies Lists:')
for movie in range(len(movie_half_url)):
    
    movies_download_url = movie_half_url[movie]+'-'+movie_full_title[movie]

    #Movies Name Lists
    movies_names = (movie_full_title[movie])

    print(movies_names)

    movie_name_and_url[movies_names] = movies_download_url

print('\n')
print('Just Copy & Paste The Movie Name')

get_movie_name = input("Enter Movie Name : ")

form = {
    'd':movie_name_and_url[get_movie_name],
    'allowCookies':'on'}

h={    
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
}

r = requests.post(url=url,data=form,headers=h).content

soup = BeautifulSoup(r, 'lxml')

for torrent in soup.find_all('a',{'title':'Download attachment'}):
    torrent_link = torrent.get('href')
    download_movie = proxysite+torrent_link

print()
print('Torrent URL Fetched : {}'.format(download_movie))
print()
print('Please Wait..')
print('URL Opening On Your Favourite Browser.')

browser = webdriver.Firefox(executable_path = 'C:\\geckodriver.exe')
#browser.get(proxysite)
browser.get(download_movie)
time.sleep(3)

login = browser.find_element_by_xpath('/html/body/div/main/div[1]/div/div[3]/form/div[2]/button')
login.submit()
