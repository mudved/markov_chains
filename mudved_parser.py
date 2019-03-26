import requests
import os
from random import choice
from bs4 import BeautifulSoup
from mudved_parser_sql import *

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

def parser(url, donor, use_proxy=False):
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
    
    title= soup.find('title').text.strip()
    description = soup.find('meta', {"name":"description"})['content']
    video = soup.find('meta', {"property":"og:video"})['content']
    image = soup.find('meta', {"property":"og:image"})['content']
    h1 = soup.find('span', id = "news-title").text.strip()
    content = soup.find('div', class_="post_content cf").text.strip()
    category = soup.find_all('span', itemprop="title")[1].text.strip()
    tags = soup.find('meta', {"name":"news_keywords"})['content'].split(',')
    result = {'h1':h1, 'title':title, 'description':description, 'video':video, 'image':image, 'content':content, 'category':category, 'tags':tags}

    return result

def spider_index(site_url):

    if not os.path.exists('parser_data\parserDB'):
        print('DB parserDB is not exist')
        create_db_parser()

    conn = sqlite3.connect(r'parser_data\parserDB')

    index_html = get_html(site_url)
    index_soup = BeautifulSoup(index_html, 'lxml')
    cats = index_soup.find('div', class_="sidebar_menu side_block").find_all('a')
    for cat in cats:
        cat_url = site_url + cat['href']
        print('START parsing: ', cat_url)
        spider_cat_page(cat_url, site_url, conn)

    conn.close()
    print('Parsing site ', site_url, ' is completed')

def spider_cat_page(cat_url, donor, conn):
    '''Парсит страницы категорий и страницы с контентом'''

    for i in range(1, 500):
        cat_page_url = cat_url + 'page/' + str(i) + '/'
        cat_page_html = get_html(cat_page_url)
        cat_page_soup = BeautifulSoup(cat_page_html, 'lxml')
        if not cat_page_soup.find('h1', class_="post_title") is None:
            print("END parsing cat: ", cat_url)
            break
        print("Parsing url: ", cat_page_url)
        page_urls = cat_page_soup.find_all('a', class_="short_post post_img")
        for page_url in page_urls:
            url = page_url['href']
            result = parser(url, donor)
            write_in_db(conn, result, url, donor)


def write_in_db(conn, result, url, donor):
    '''Записывает в БД результаты парсинга страницы'''

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
    spider_index('http://pornolomka.me')


if __name__ == '__main__':
    main()
