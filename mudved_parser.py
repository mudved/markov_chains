import requests
from random import choice
from bs4 import BeautifulSoup

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
    index_html = get_html(site_url)
    index_soup = BeautifulSoup(index_html, 'lxml')
    cats = index_soup.find('div', class_="sidebar_menu side_block").find_all('a')
    for cat in cats:
        cat_url = site_url + cat['href']
        print('START parsing: ', cat_url)
        spider_cat_page(cat_url)

def spider_cat_page(cat_url):
        for i in range(180, 200):
            cat_page_url = cat_url + 'page/' + str(i) + '/'
            cat_page_html = get_html(cat_page_url)
            cat_page_soup = BeautifulSoup(cat_page_html, 'lxml')
            if not cat_page_soup.find('h1', class_="post_title") is None:
                print("END parsing cat: ", cat_url)
                break
            print("Parsing url: ",cat_page_url)
            page_urls = cat_page_soup.find_all('a', class_="short_post post_img")
            for page_url in page_urls:
                url = page_url['href']



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
