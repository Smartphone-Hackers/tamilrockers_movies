import requests
import os
import shutil
import time
import re
from progress.bar import Bar
from bs4 import BeautifulSoup
from selenium import webdriver

def main():

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

    count = 1

    os.mkdir('Smartphone Hackers')
    os.chdir('Smartphone Hackers')

    movie_name_scraped_file = open('movie_name_lists.txt','a')
    movie_id_generate = open('movie_id.txt','a')

    print('Please Wait Movies Name Scraping...')
    print('Its Take 3-5 minutes..')

    b = Bar('Loading : ',max=49)

    for i in range(1,50):

        b.next()

        form = {
            'd':'{}/index.php/forum/115-tamil-new-dvdrips-hdrips-bdrips-movies/page-{}?prune_day=100&sort_by=Z-A&sort_key=last_post&topicfilter=all'.format(tamilrockers_domain_name,i),
            'allowCookies':'on'
        }

        more_movies = requests.post(url=url, data=form).content

        soup = BeautifulSoup(more_movies,'lxml')

        div_tag = soup.find_all('div',{"class":"ipsBox_container"})

        for div in div_tag:
        
            title_gen = div.find_all('span',{"itemprop":"name"})

            for title in title_gen:

                t = title.text
                k = ''.join(re.findall(r'[^\(\)\[\]-]',t))

                movie_name_scraped_file.write('\n' + k.replace('  ',' ').replace('.','').replace(' ','-').lower())
                count = count + 1

            a_tag = div.find_all('a') 

            for a in a_tag:
                movie_id = a.get('id')
                            
                if movie_id != None:           
                    id_gen = movie_id.split('-')[-1]
                    
                    if id_gen.isdigit():

                        movie_id_generate.write('\n' + tamilrockers_domain_name+'/index.php/topic/'+id_gen)

    b.finish()
    print("Completed!")

def movies_and_ids():

    movie_name_and_url = {}

    os.chdir('Smartphone Hackers')

    file1 = open('movie_name_lists.txt').readlines()

    file2 = open('movie_id.txt').readlines()

    for f1 in range(len(file1)):

        f1_strip = file1[f1].strip()
        f2_strip = file2[f1].strip()
        
        movies_download_url = f2_strip+'-'+f1_strip

        movies_names = f1_strip

        movie_name_and_url[movies_names] = movies_download_url

    return movie_name_and_url

def remove_dupicate():

    path = os.getcwd()

    for roots,dirs,files in os.walk(path):

        for di in dirs:
        
            if di == 'Smartphone Hackers':
        
                try:
                    shutil.rmtree('Smartphone Hackers')
        
                except:
                    print("Please Remove ['Smartphone Hackers'] Folder!")

if __name__ == '__main__':
    remove_dupicate()
    main()