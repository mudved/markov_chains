import re
import requests
from settings import *

def get_ip(html):
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('span', class_='ip').text.strip()
    ua = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
    print(ip)
    print(ua)

def strip_list(items):
    '''Функция чистки элементов списка'''
    
    clear_list = []
    for item in items:
        item = item.strip()
        clear_list.append(item)
    return clear_list

def get_donor_url(url):
    '''Функция получения адреса донора'''

    protokol = url.split('//')[0]
    domain = url.split('//')[1].split('/')[0]
    donor = protokol + '//' + domain
    return donor

def do_reg(html, donor, reg_template):
    '''Функция выполняет регулярное выражение и возвращает найденную, либо пустую строку'''

    try:
        reg_result = re.search(PARSING_PAGE_SETTINGS[donor][reg_template], html)[0].strip()
    except:
        reg_result = ''
        if reg_template != 'error_reg':
            print('{} not found'.format(reg_template))
    return reg_result

def do_reg_list(html, donor, reg_template_all, reg_template):
    '''Функция выполняет регулярные выражения и возвращает найденный, либо пустой список результатов'''

    try:
        all_items = re.search(PARSING_PAGE_SETTINGS[donor][reg_template_all], html, re.S)[0]
        items = re.findall(PARSING_PAGE_SETTINGS[donor][reg_template], all_items)
        reg_result = strip_list(items)
    except:
        reg_result = []
        print('{} not found'.format(reg_template))
    return reg_result

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
        try:
            r = requests.get(url)
        except:
            print("Error get html for url: ", url)
            with open(r'parser_data\pages_urls_bad.txt', 'a') as file:
                file.write(url +'\n')

            return False

    return r.text
