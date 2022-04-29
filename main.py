import requests
import bs4
import re
from datetime import datetime
from useragent import user_agent

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
PATTERN = r'(\W|^)(дизайн|фото|web|python)(\W|$)'


def print_result():
    artical_date = artical.find(class_='tm-article-snippet__datetime-published')
    artical_date = artical_date.time.get('title')
    artical_date = datetime.date(datetime.strptime(artical_date, '%Y-%m-%d, %H:%M')).strftime('%d.%m.%Y')
    print(f"{artical_date} {__url_habr + artical.h2.a.get('href')} {artical.h2.text}")


if __name__ == '__main__':

    __url_habr_all = 'https://habr.com/ru/all'
    __url_habr = 'https://habr.com'

    re_obj = re.compile(PATTERN, flags=re.I)

    resp = requests.get(__url_habr_all, headers=user_agent)
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    articals = soup.find_all('article')

    for artical in articals:
        body = artical.find(class_='article-formatted-body')
        if re_obj.search(body.text) or re_obj.search(artical.h2.text):
            print_result()
            continue

        hubs = artical.find_all(class_='tm-article-snippet__hubs')
        for hub in hubs:
            if re_obj.search(hub.span.text):
                print_result()
                break
            continue

        resp = requests.get(__url_habr + artical.h2.a.get('href'), headers=user_agent)
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')
        body = soup.find(class_='tm-article-body')
        if re_obj.search(body.text):
            print_result()


