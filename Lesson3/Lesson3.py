from urllib.parse import urljoin
import bs4
import time
import typing
import requests
import pymongo
from database.database import Database

"""
1. Открыть точку входа
2. Скопировать список ссылок на статьи (вытесненение. удаление отработанной ссылки)
3. Перейти/Открыть ссылку на статью из списка
4. Извлечь необходимую по требованию информацию
5. Сохранить информацию в БД
6. Перейти к шагу 3, со следующей ссылкой (пока не закончатся повторяем)
7. Переход к шагу 1 с точкой входа след странички пагиниации (поыторять пока не закончатся)

- Пагинируемые страницы:
1. Извлечь ссылки на статьи
1.1. Породить в очереди задач задачи
2. Извлечь ссылки на статьи
2.1. Породить в очереди задач задачи

- Страница Поста
составить структуру информации (извлечь данные)
Сохранить структуру данных

url = 'https://gb.ru/posts'

response = requests.get(url)
soup = bs4.BeautifullSoup(response.text, 'lxml')

"""


class GBParseLess2:
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64; rv: 89.0) Gecko / 20100101 Firefox / 89.0'
    }
    __parse_time = 0

    def __init__(self, start_url, db: Database, delay=1.0):
        self.start_url = start_url
        self.db = db
        self.delay = delay
        self.done_url = set()
        self.tasks: typing.List[typing.Callable] = []
        self.task_creator({self.start_url, }, self.parse_feed)
        self.save = _save()

    def _get_response(self, url):
        while True:
            next_time = self.__parse_time + self.delay
            if next_time > time.time():
                time.sleep(next_time - time.time())
            response = requests.get(url, headers=self.headers)
            print(f"RESPONSE: {response.url}")
            self.__parse_time = time.time()
            if response.status_code == 200:
                return response

    def get_task(self, url: str, callback: typing.Callable):
        def task():
            response = self._get_response(url)
            return callback(response)

        return task()

    def run(self):
        while True:
            try:
                task = self.tasks.pop(0)
            except IndexError:
                break

    def task_creator(self, urls: set, callback):
        urls_set = urls - self.done_url
        for url in urls_set:
            self.tasks.append(
                self.get_task(url, callback)
            )
            self.done_url.add(url)

    def parse_feed(self, response: requests.Response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        ul_pagination = soup.find('ul', attrs={"class": "gb__pagination"})
        self.task_creator(
            {urljoin(response.url, a_tag.attrs['href']) for a_tag in ul_pagination.find_all('a')
             if a_tag.attrs.get('href')},
            self.parse_feed,
        )

        post_wrapper = soup.find('div', attrs={'class': 'post-items-wrapper'})
        self.task_creator(
            {urljoin(response.url, a_tag.attrs['href'])
             for a_tag in post_wrapper.find_all('a', attrs={'class': 'post_item__title'})
             if a_tag.attrs.get('href')},
            self.parse_post,
        )

    def parse_post(self, response: requests.Response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        author_name_tag = soup.find('div', itemprop='author')
        data = {
            'post_data':{
                'title': soup.find('h1', attrs={'class': 'blogpost-title'}).text,
                'url': response.url,
                'id': int(soup.find('comments').attrs.get('commentable-id')),
            },
            'author_data': {
                'url': urljoin(response.url, author_name_tag.parent.attrs.get('href')),
                'name': author_name_tag.text,
            },
            'tags_data': [
                {'name': tag.text, 'url': urljoin(response.url, tag.attrs.get('href'))}
                for tag in soup.find_all('a', attrs={'class': 'small'})
            ],
            'comments_data': self._get_response(soup.find('comments').attrs.get('commentable-id'))
        }
            #self._save(data)


    def _get_comments(self, post_id):
        api_path = f'/api/v2/comments?commentable_type=Post&commentable_id={post_id}&order=desc'
        response = self._get_response(urljoin(self.start_url, api_path))
        data = response.json()
        return data

""" форма save для урока №2
    def _save(self, data):
        collection = self.db['gb_parse_less2']['gb_parse']
        collection.insert_one(data)
"""
# форма save для урока №3
    def _save(self, data):
        #collection = self.db['gb_parse_less2']['gb_parse']
        #collection.insert_one(data)
        self.db.add_post(data) # вариант save для 3-го урока

if __name__ == '__main__':
    db_client = Database('sqlite:///gb_blog.db')
    parser = GBParseLess2('https://gb.ru/posts', db_client, 0.5)
    parser.run()
