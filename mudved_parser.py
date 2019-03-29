import requests
import os
import re
import time
import random
from random import choice
from bs4 import BeautifulSoup
from multiprocessing import Pool
from mudved_parser_sql import *
from settings import *
from utils import *

def get_html(url, use_proxy = False, try_count = 10):
    '''Получает текст html страницы по url-адресу
    try_count - количество попыток использовать прокси'''

    if use_proxy:
        useragents = open(r'parser_data\useragents.txt').read().split('\n')
        proxies = open(r'parser_data\proxies.txt').read().split('\n')
        for i in range(int(try_count)):
            proxy = {'http': 'http://' + choice(proxies)}
            useragent = {'User-Agent': choice(useragents)}
            try:
                r = requests.get(url, headers=useragent, proxies=proxy)
            except:
                continue
            else:
                print("Used proxy: ", proxy)
                break
    else:
        print("Proxy not use.")
        try:
            r = requests.get(url)
        except:
            print("Error get html for url: ", url)
            with open(r'parser_data\pages_urls_bad.txt', 'a') as file:
                file.write(url +'\n')

            return False

    return r.text

def parser_page(url, use_proxy=False):
    '''Функция для парсинга страниц доноров основана на BeautifulSoup'''

    print("Start parsing: ", url)
    html = get_html(url, use_proxy)
    if not html:
        return False

    with open(r'parser_data\pages_urls_parsed.txt', 'a') as file:
        file.write(url +'\n')

    soup = BeautifulSoup(html, 'lxml')
    donor = get_donor_url(url)

    if donor == 'http://pornolomka.me/':
        try:
            video = soup.find('meta', {"property":"og:video"})['content']
        except:
            video = ''
            print("Video not found")
        try:
            image = soup.find('meta', {"property":"og:image"})['content']
        except:
            image = ''
            print("Image not found")

    elif donor == 'https://www.pornolomka.info/':
        try:
            video = soup.find('div', {"class":"post_content cf"}).find("script").text
            video = re.search(r'http.*(?="})', video)[0]
        except:
            video = ''
            print("Video not found")
        try:
            image = soup.find('meta', {"property":"og:image"})['content']
        except:
            image = ''
            print("Image not found")

    try:
        title= soup.find('title').text.strip()
    except:
        title = ''
        print("Title not found")
    try:
        description = soup.find('meta', {"name":"description"})['content']
    except:
        description = ''
        print("Description not found")
    try:
        h1 = soup.find('span', id = "news-title").text.strip()
    except:
        h1 = ''
        print("H1 not found")
    try:
        content = soup.find('div', class_="post_content cf").text
        content = re.split(r'var', content)[0].strip()
    except:
        content = ''
        print("Content not found")
    try:
        categories = []
        #tags_a = soup.findAll('div', class_='info-col1')[1].findAll('div', class_="col2-item")[2].findAll('a')
        tags_a = soup.findAll('div', class_='info-col1')[1].findAll('div', class_="col2-item")
        for b in tags_a:
            temp = b.findAll('a')
            if temp != []:
                for temp2 in temp:
                    cat = temp2.text.strip()
                    categories.append(cat)
                break
    except:
        categories = [] 
        print("Category not found")
    try:
        tags = []
        all_tags = soup.find('meta', {"name":"news_keywords"})['content'].split(',')
        for tag in all_tags:
            tag = tag.strip()
            tags.append(tag)
    except:
        tags = []
        print("Tags not found")

    try:
        actors = []
        actors_a = soup.findAll('div', class_='info-col1')[1].findAll('div', class_="col2-item")
        for b in actors_a:
            temp = b.findAll('a')
            if temp != []:
                for temp2 in temp:
                    actor = temp2.text.strip()
                    if (actor not in tags) and (actor not in categories):
                        actors.append(actor)
    except:
        actors = []
        print("Actors not found")

    result = {'h1':h1, 
              'title':title, 
              'description':description, 
              'video':video, 
              'image':image, 
              'content':content, 
              'categories':categories, 
              'tags':tags, 
              'actors':actors}

    return result

def get_cats_urls(index_url):
    '''Получает url-ы категорий сайта'''

    index_html = get_html(index_url)
    index_soup = BeautifulSoup(index_html, 'lxml')
    try:
        if index_url == 'http://pornolomka.me' or index_url == 'https://www.pornolomka.info':
            cats = index_soup.find('div', class_="sidebar_menu side_block").find_all('a')
        elif index_url == 'https://www.poimel.cc':
            cats = index_soup.find('div', class_="left-mnu").find_all('a')

    except:
        print("Error cats parsing")
        return False

    cats_urls = []

    for cat in cats:
        cat_url = index_url + cat['href']
        cats_urls.append(cat_url)

    return cats_urls

def get_cat_pages(cat_url):
    '''Парсит страницы категорий и возвращает список ссылок на все страницы категории'''

    pages_urls = []
    with open(r'parser_data\pages_urls_parsed.txt', 'r') as file:
        pages_urls_parsed = file.read().splitlines()

    for i in range(1, 500):
        cat_page_url = cat_url + 'page/' + str(i) + '/'
        cat_page_html = get_html(cat_page_url)
        cat_page_soup = BeautifulSoup(cat_page_html, 'lxml')

        if not cat_page_soup.find('h1', class_="post_title") is None:
            print("END parsing CATEGORY: ", cat_url)
            break

        print("Parsing urls from page №", i, end = '\r')
        try:
            urls_on_page = cat_page_soup.find_all('a', class_="short_post post_img")
        except:
            print("Error parsing page ", cat_page_url)
            return False

        for url_page in urls_on_page:
            url = url_page['href']
            if url not in pages_urls_parsed:
                pages_urls.append(url)

    pages_urls = list(set(pages_urls))
    return pages_urls

def make_all(page_url):
    '''Функция для запуска парсинга в несколько потоков'''

    result = parser_page(page_url, False)

    if not result:
        return False

    time.sleep(random.randint(1,5))
    write_in_db(result, page_url)
    with open('generator_data\parsingdata.txt', 'a') as file:
        if result['content'] != '':
            file.write(result['content']+'\n')

    return True

def multy_parser(site_url, streams=3):
    '''Мульти-парсер в несколько потоков
    streams - количество потоков парсинга страниц'''

    if not os.path.exists('parser_data\parserDB'):
        print('DB parserDB is not exist')
        create_db_parser()

    cats_urls = get_cats_urls(site_url)
    if not cats_urls:
        return False

    print('There are ', str(len(cats_urls)), ' CATEGORIES in site ', site_url)
    
    pages_urls = []

    for cat_url in cats_urls:
        print('START parsing CATEGORY: ', cat_url)
        cat_pages_urls = get_cat_pages(cat_url)
        if not cat_pages_urls:
            print("Error parsing category ", cat_url)
            continue

        print('There are ', str(len(cat_pages_urls)), ' PAGES in CATEGORY ', cat_url)
        pages_urls = list(set(pages_urls + cat_pages_urls))

    print('There are ', str(len(pages_urls)), ' unique PAGES in site', site_url)
    with open(r'parser_data\pages_urls.txt', 'a') as file:
        file.write('\n'.join(pages_urls))

    with Pool(streams) as p:
        p.map(make_all, pages_urls)

    print('Parsing site ', site_url, ' is completed')
    return True

def parser(site_url):
    '''Главный парсер'''

    if not os.path.exists('parser_data\parserDB'):
        print('DB parserDB is not exist')
        create_db_parser()

    cats_urls = get_cats_urls(site_url)
    if not cats_urls:
        return False

    print('There are ', str(len(cats_urls)), ' CATEGORIES in site ', site_url)
    
    pages_urls = []

    for cat_url in cats_urls:
        print('START parsing CATEGORY: ', cat_url)
        cat_pages_urls = get_cat_pages(cat_url)
        if not cat_pages_urls:
            return False

        print('There are ', str(len(cat_pages_urls)), ' PAGES in CATEGORY ', cat_url)
        pages_urls = list(set(pages_urls + cat_pages_urls))

    print('There are ', str(len(pages_urls)), ' unique PAGES in site', site_url)
    with open(r'parser_data\pages_urls.txt', 'a') as file:
        file.write('\n'.join(pages_urls))

    error_count = 0
    for page_url in pages_urls:
        result = parser_page(page_url, True)

        if not result:
            error_count += 1
            if error_count > 5:                  #Если подряд идут 5 ошибок 
                print("STOP parsing")
                return False
            continue

        error_count = 0
        write_in_db(result, page_url)
        with open('generator_data\parsingdata.txt', 'a') as file:
            file.write(result['content']+'\n')

    print('Parsing site ', site_url, ' is completed')
    return True

def parser_page_reg(url, use_proxy = False):
    '''Функция для парсинга страниц доноров регулярками'''

    print("Start parsing (reg mode): ", url)
    html = get_html(url, use_proxy)

    if not html:
        return False
    
    with open(r'parser_data\pages_urls_parsed.txt', 'a') as file:
        file.write(url +'\n')

    donor = get_donor_url(url)
    title = do_reg(html, donor, 'title_reg')
    description = do_reg(html, donor, 'description_reg')
    h1 = do_reg(html, donor, 'h1_reg')
    content = do_reg(html, donor, 'content_reg')
    video = do_reg(html, donor, 'video_reg')
    image = do_reg(html, donor, 'image_reg')
    categories = do_reg_list(html, donor, 'all_categories_reg', 'categories_reg')
    tags = do_reg_list(html, donor, 'all_tags_reg', 'tags_reg')
    actors = do_reg_list(html, donor, 'all_actors_reg', 'actors_reg')

    result = {'h1':h1, 
              'title':title, 
              'description':description, 
              'video':video, 
              'image':image, 
              'content':content, 
              'categories':categories, 
              'tags':tags, 
              'actors':actors}

    return result

def main():

    #res = parser('http://pornolomka.me')
    #res = multy_parser('http://pornolomka.me', 4)
    #res = multy_parser('https://www.pornolomka.info', 4)
    #res = parser('https://www.poimel.cc')
    #res = parser('https://www.pornolomka.info')
    #print(res)
    #result = parser_page_reg('https://www.pornolomka.info/11303-grudastaja-telka-drochit-ljubimym-dyldo.html')
    #print(result)
    result2 = parser_page_reg('http://pornolomka.me/8352-pokazala-kak-byt-lesbiyankoy.html')
    print(result2)

if __name__ == '__main__':
    main()

