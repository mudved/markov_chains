import requests
from bs4 import BeautifulSoup

def get_html(url):
    '''Получаем текст html страницы по url-адресу'''

    r = requests.get(url)
    return r.text

def get_ip(html):
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('span', class_='ip').text.strip()
    ua = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
    print(ip)
    print(ua)


def get_proxylist():
    url = 'https://free-proxy-list.net'
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    for i in range(1, 20):
        ip = soup.findAll('tr')[i].next_sibling('td')[0].text.strip()
        port =soup.findAll('tr')[i].next_sibling('td')[1].text.strip()
        print(ip)
        print(port)



def main():
    #html = get_html('http://sitespy.ru/my-ip')
    #get_ip(html)
    get_proxylist()

if __name__ == '__main__':
    main()
