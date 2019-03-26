import requests
import os
from random import choice
from bs4 import BeautifulSoup
from mudved_parser_sql import *
from multiprocessing import Pool

def get_html(url, useragent=None, proxy=None):
    '''Получает текст html страницы по url-адресу'''

    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text

def get_ip(html):
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('span', class_='ip').text.strip()
    ua = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
    print(ip)
    print(ua)

def parser_page(url, donor, use_proxy=False):
    '''Функция для парсинга страниц доноров'''

    print("Start parsing: ", url)
    if use_proxy and get_proxylist():
        print("Proxy parsing completed.")
        useragents = open(r'parser_data\useragents.txt').read().split('\n')
        proxies = open(r'parser_data\proxies.txt').read().split('\n')
        for i in range(10):
            proxy = {'http': 'http://' + choice(proxies)}
            useragent = {'User-Agent': choice(useragents)}
            try:
                html = get_html(url, useragent, proxy)
            except:
                continue
            else:
                print("Used proxy: ", proxy)
                break
    else:
        print("Proxy not use.")
        html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')
    
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
        video = soup.find('meta', {"property":"og:video"})['content']
    except:
        video = ''
        print("Video not found")
    try:
        image = soup.find('meta', {"property":"og:image"})['content']
    except:
        image = ''
        print("Image not found")
    try:
        h1 = soup.find('span', id = "news-title").text.strip()
    except:
        h1 = ''
        print("H1 not found")
    try:
        content = soup.find('div', class_="post_content cf").text.strip()
    except:
        content = ''
        print("Content not found")
    try:
        category = soup.find_all('span', itemprop="title")[1].text.strip()
    except:
        category = ''
        print("Category not found")
    try:
        tags = soup.find('meta', {"name":"news_keywords"})['content'].split(',')
    except:
        tags = []
        print("Tags not found")

    result = {'h1':h1, 'title':title, 'description':description, 'video':video, 'image':image, 'content':content, 'category':category, 'tags':tags}

    return result


def get_cats_urls(index_url):
    '''Получает url-ы категорий сайта'''

    index_html = get_html(index_url)
    index_soup = BeautifulSoup(index_html, 'lxml')
    try:
        cats = index_soup.find('div', class_="sidebar_menu side_block").find_all('a')
    except:
        print("Error cats parsing")

    cats_urls = []

    for cat in cats:
        cat_url = index_url + cat['href']
        cats_urls.append(cat_url)

    return cats_urls

def get_cat_pages(cat_url):
    '''Парсит страницы категорий и возвращает список ссылок на все страницы категории'''

    pages_urls = []

    for i in range(1, 500):
        cat_page_url = cat_url + 'page/' + str(i) + '/'
        cat_page_html = get_html(cat_page_url)
        cat_page_soup = BeautifulSoup(cat_page_html, 'lxml')
        if not cat_page_soup.find('h1', class_="post_title") is None:
            print("END parsing CATEGORY: ", cat_url)
            break
        print("Parsing page №", i)
        try:
            urls_on_page = cat_page_soup.find_all('a', class_="short_post post_img")
        except:
            print("Error parsing page ", cat_page_url)

        for url_page in urls_on_page:
            url = url_page['href']
            pages_urls.append(url)

    return pages_urls

def make_all(url):
    pass



def parser(site_url):
    '''Главный парсер'''

    if not os.path.exists('parser_data\parserDB'):
        print('DB parserDB is not exist')
        create_db_parser()

    #conn = sqlite3.connect(r'parser_data\parserDB')

    cats_urls = get_cats_urls(site_url)
    print('There are ', str(len(cats_urls)), ' CATEGORIES in site ', site_url)
    
    for cat_url in cats_urls:
        print('START parsing CATEGORY: ', cat_url)
        pages_urls = get_cat_pages(cat_url)
        print('There are ', str(len(pages_urls)), ' PAGES in CATEGORY ', cat_url)

        for page_url in pages_urls:
            print('parsing PAGE url: ', page_url)
            result = parser_page(page_url, site_url)
            write_in_db(result, page_url, site_url)
            with open('generator_data\parsingdata.txt', 'a') as file:
                file.write(result['content'])

    #conn.close()
    print('Parsing site ', site_url, ' is completed')
    return True

def write_in_db(result, url, donor):
    '''Записывает в БД результаты парсинга страницы'''

    conn = sqlite3.connect(r'parser_data\parserDB')

    options = {'url':url}
    id_url= input_db(conn, 'url', options)

    options = {'category':result['category']}
    id_category= input_db(conn, 'category', options)

    options = {'donor':donor}
    id_donor= input_db(conn, 'donor', options)

    options = {'image':result['image']}
    id_image= input_db(conn, 'image', options)

    options = {'video':result['video']}
    id_video= input_db(conn, 'video', options)

    options = {'key':result['h1']}
    id_key= input_db(conn, 'key', options)

    options = {'cat_id':id_category, 'url_id':id_url, 'title':result['title'], 'description':result['description'], 'h1':result['h1'], 'content':result['content']}
    id_content= input_db(conn, 'content', options)

    options = {'content_id':id_content, 'donor_id':id_donor}
    id_content_donor= input_db(conn, 'content_donor', options)
    
    options = {'content_id':id_content, 'image_id':id_image}
    id_content_image= input_db(conn, 'content_image', options)

    options = {'content_id':id_content, 'key_id':id_key}
    id_content_key= input_db(conn, 'content_key', options)

    options = {'content_id':id_content, 'video_id':id_video}
    id_content_video= input_db(conn, 'content_video', options)

    for tag in result['tags']:
        options = {'tag':tag}
        id_tag = input_db(conn, 'tag', options)
        
        options = {'content_id':id_content, 'tag_id':id_tag}
        id_content_tag = input_db(conn, 'content_tag', options)
    print('Write in DB ***************** OK')

    conn.close()
    
def get_proxylist():
    '''Парсит список прокси и портов и записывает в файл
    возвращает True, если удалось записать хотя бы 1 прокси'''

    print("Start proxy parsing")
    url = 'https://free-proxy-list.net'
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    with open(r'parser_data\proxies.txt', 'w') as f:
        first = True
        for i in range(1, 20):
            ip = soup.findAll('tr')[i].next_sibling('td')[0].text.strip()
            port = soup.findAll('tr')[i].next_sibling('td')[1].text.strip()
            yes =  soup.findAll('tr')[i].next_sibling('td')[6].text.strip()
            if yes == 'no' and not first:
                proxy = '\n{0}:{1}'.format(ip, port)
                f.write(proxy)
            elif yes == 'no' and first:
                proxy = '{0}:{1}'.format(ip, port)
                first = False
                f.write(proxy)

    return not first

def main():
    #if True or get_proxylist():
    #    print("Proxy parsing completed.")
    #    useragents = open(r'parser_data\useragents.txt').read().split('\n')
    #    proxies = open(r'parser_data\proxies.txt').read().split('\n')
    #    for i in range(10):
    #        proxy = {'http': 'http://' + choice(proxies)}
    #        useragent = {'User-Agent': choice(useragents)}
    #        try:
    #            html = get_html('http://sitespy.ru/my-ip', useragent, proxy)
    #        except:
    #            continue
    #        else:
    #            break
    #else:
    #    print("Proxy parsing not completed.")
    #    html = get_html('http://sitespy.ru/my-ip')
    #get_ip(html)
    #result = parser('http://pornolomka.me/8285-pizda-krupno-posle-seksa.html', 'pornolomka.me')
    #print(result)
    parser('http://pornolomka.me')


if __name__ == '__main__':
    main()
