import movies_scrap
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

url = "https://eu0.proxysite.com/includes/process.php?action=update"

proxysite = "https://eu0.proxysite.com"

movie_name_and_url = movies_scrap.movies_and_ids()

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