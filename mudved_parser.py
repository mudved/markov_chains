import requests
import os
import re
import time
import random
from random import choice
from multiprocessing import Pool
from mudved_parser_sql import *
from settings import *
from utils import *

def get_cats_urls_reg(index_url):
    '''Получает url-ы категорий сайта'''

    index_html = get_html(index_url, False)
    
    cats = do_reg_list(index_html, index_url, 'all_categories_url_reg', 'categories_url_reg')
    cats_urls = []

    for cat in cats:
        cat_url = index_url + cat
        cats_urls.append(cat_url)

    return cats_urls

def get_pages_urls_reg(cat_url, count_pages = 500):
    '''Парсит страницы категорий и возвращает список ссылок на все страницы категории
    count_pages - количество страниц категории, которые нужно обойти'''

    pages_urls = []
    donor = get_donor_url(cat_url)
    with open(r'parser_data\pages_urls_parsed.txt', 'r') as file:
        pages_urls_parsed = file.read().splitlines()

    for i in range(1, int(count_pages + 1)):
        cat_page_url = cat_url + 'page/' + str(i) + '/'
        cat_page_html = get_html(cat_page_url, False)
        error = do_reg(cat_page_html, donor, 'error_reg')
        if error != '':
            print("END parsing CATEGORY: ", cat_url)
            break

        print("Parsing urls from page №", i, end = '\r')
        urls_on_page = do_reg_list(cat_page_html, donor, 'all_pages_url_reg', 'pages_url_reg')

        for url_page in urls_on_page:
            url = url_page.strip()
            if url not in pages_urls_parsed:
                pages_urls.append(url)

    pages_urls = list(set(pages_urls))
    return pages_urls

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

def make_all_reg(page_url):
    '''Функция для запуска парсинга в несколько потоков'''

    result = parser_page_reg(page_url, False)

    if not result:
        return False

    time.sleep(random.randint(1,3))
    write_in_db(result, page_url)
    with open('generator_data\parsingdata.txt', 'a') as file:
        if result['content'] != '':
            file.write(result['content']+'\n')

    return True

def multy_parser_reg(site_url, streams = 3):
    '''Мульти-парсер в несколько потоков
    streams - количество потоков парсинга страниц'''

    if not os.path.exists('parser_data\parserDB'):
        print('DB "parserDB" is not exist')
        create_db_parser()

    cats_urls = get_cats_urls_reg(site_url)
    if cats_urls == []:
        print('Categories not found')
        return False

    print('Found ', str(len(cats_urls)), ' CATEGORIES in site ', site_url)
    
    pages_urls = []

    for cat_url in cats_urls:
        print('START parsing CATEGORY: ', cat_url)
        cat_pages_urls = get_pages_urls_reg(cat_url)
        if not cat_pages_urls:
            print("Error parsing category ", cat_url)
            continue

        print('Found ', str(len(cat_pages_urls)), ' PAGES in CATEGORY ', cat_url)
        pages_urls = list(set(pages_urls + cat_pages_urls))

    print('Found ', str(len(pages_urls)), ' unique PAGES in site', site_url)
    with open(r'parser_data\pages_urls.txt', 'a') as file:
        file.write('\n'.join(pages_urls))

    with Pool(streams) as p:
        p.map(make_all_reg, pages_urls)

    print('Parsing site ', site_url, ' is COMPLETED')
    return True

def test_reg(url):
    '''Функция для тестирования настроек регулярных выражений для сайта'''

    print("************************")
    print("* Result parsing page: *")
    print("************************")
    res = parser_page_reg(url, False)
    print(res)
    print("******************************")
    print("* Result parsing categories: *")
    print("******************************")
    cats = get_cats_urls_reg(get_donor_url(url))
    print("Parsing ", str(len(cats)), " categories.")
    print(cats)
    print("*************************************")
    print("* Result parsing urls from cat page *")
    print("*************************************")
    urls = get_pages_urls_reg(cats[1], 1)
    print("Parsing ", str(len(urls)), " pages in category ", cats[1])
    print(urls, '\n')

def main():

    #res = multy_parser_reg('http://pornolomka.me', 4)
    res = multy_parser_reg('https://www.pornolomka.info', 4)
    #('https://www.poimel.cc')
    #('https://www.pornolomka.info')
    #test_reg('http://pornolomka.me/8372-chb-domashka.html')
    #test_reg('https://www.pornolomka.info/11303-grudastaja-telka-drochit-ljubimym-dildo.html')

if __name__ == '__main__':
    main()
