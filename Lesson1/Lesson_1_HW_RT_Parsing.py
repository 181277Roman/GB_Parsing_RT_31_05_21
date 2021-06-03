from pathlib import Path
import requests
import time
import json
from bs4 import BeautifulSoup


url = "https://5ka.ru/special_offers/"

headers = {
    'User-Agent': 'FireFox'
}

params = {
    'store':'X326',
    'records_per_page' :12,
    'page':1,
    'categories': None,
    'ordering': None,
    'price_promo__gte': None,
    'price_promo__lte': None,
    'search': None
}

response = requests.get(url, headers=headers)

test_file = Path(__file__).parent.joinpath('test_file.html')
test_file.write_bytes(response.content)

class ParserShop5:
    headers = {
        'User-Agent': 'FireFox'
    }
    def __init__(self, start_url: str, save_dir: Path):
        self.start_url = start_url
        self.save_dir = save_dir

    def _get_response(self, url: str):
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.2)

    def run(self):
        for product in self._parse(self.start_url):
            file_name = f'{product["id"]}.json' # форма генерации файла по id  с сайта
            file_path = self.save_dir.joinpath(file_name) # файл продукта
            self._save(product, file_path) # сохранение файла в директорию product

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data = response.json()
            url = data['next']
            for product in data['results']:
                yield product

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data))

# начало блока ДЗ
class CatParser(ParserShop5):

    def __init__(self, categories_url, *args, **kwargs):
        self.categories_url = categories_url
        super().__init__(*args, **kwargs)

    def _get_cat(self):
        response = self._get_response(self.categories_url)
        data = response.join()
        return data

    def run(self):
        for category in self._get_cat():
            category['products'] = [] # категория продукта с сайта для сборки url
            params = f"?categories={category['parent_group_code']}" # ссылка на категорию для сборки url ниже
            url = f"{self.start_url}{params}"

            category["products"].extend(list(self._parse(url)))
            file_name_cat = f"{category['parent_group_code']}.json" # создание имени файла
            cat_path = self.save_dir.joinpath(file_name_cat) # создание пути файла
            self._save(category, cat_path)

# окончание блока ДЗ


def _get_dir_path(dir_name: str):
    dir_path = Path(__file__).parent.joinpath(dir_name)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


if __name__ == '__main__':
    url = 'https://5ka.ru/api/v2/special_offers/'
    save_dir = _get_dir_path('products')
    parser = ParserShop5(url, save_dir)
    parser.run()



















"""
HOST = 'https://5ka.ru/'
URL = 'https://5ka.ru/api/v2/special_offers/?store=X326/'
headers = {
        'User-Agent': 'FireFox'
    }

def get_response(url: str, params='') -> requests.Response:  # запрос. процесс в бесконечном цикле
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:  # если статус-код - 200, то запрос возвращается
            return response
        time.sleep(0.2)  # пауза в запросе, если статус-код не 200

def get_content(html): # получение необходимого контента
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='special-offers__inner')
    category = []

    for item in items:
        category.append(
            {
                'name': item.find('div', class_='filter_menu').get_text(strip=True),
                'price': item.find('div', class_='sale-card_price-wrapper').get_text(strip=True),
                'products': item.find('div', class_='sale-card_title').get_text(strip=True),
                'image': HOST + item.find('div', class_='sale-card_img').find('img').get('src'),
            }
        )
    return category

html = get_response(URL)
print(get_content(html.text))



 url = "https://5ka.ru/special_offers/?store=310D/"

headers = {
    'User-Agent': 'FireFox'
}

params = {
    'store': None,
    'records_per_page': 12,
    'page': 1,
    'shopitem_category': None,
}

response = requests.get(url, headers=headers)  # запрос и его параметры

test_file = Path(__file__).parent.joinpath('test_file.html')
test_file.write_bytes(response.content)




class Parsing5:
    headers = {
        'User-Agent': 'FireFox'
    }

    def __init__(self, start_url: str, save_dir: Path):
        self.start_url = start_url
        self.save_dir = save_dir

    def _get_response(self, url: str) -> requests.Response:  # запрос. процесс в бесконечном цикле
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:  # если статус-код - 200, то запрос возвращается
                return response
            time.sleep(0.2)  # пауза в запросе, если статус-код не 200

    def run(self):  # параметры запуска парсера
        for product in self._parse(self.start_url):
            file_name = f"{product['id']}.json"  # формирование имени файла. id - идентификатор продукта с вэб страницы
            file_path = self.save_dir.joinpath(file_name)  # создание директории файла
            self._save(product, file_path)  # отправка продукта и созд директории

    def _parse(self, url):  # параметры парсера
        while url:
            response = self._get_response(url)
            data = response.json()
            url = data['next']  # next - см. кодировку страницы.
            for product in data['results']:  # results - категория где хранятся товары. см кодировку страницы
                yield product  # yield возвращает продукт, но не останавливает цикл

    def _save(self, data: dict, file_path: Path):  # параметры полученных данных в формате json и место хранения
        file_path.write_text(json.dumps(data, ensure_ascii=False), 'utf8')


def get_dir_path(dir_name: str) -> Path:  # принимает имя директории и возвращает путь к директории
    dir_path = Path(__file__).parent.joinpath(dir_name)
    if not dir_path.exists():  # проверка на наличие директории
        dir_path.mkdir()  # создание диретории в случае её отсутствия
    return dir_path


if __name__ == '__main__':
    url = "https://5ka.ru/api/v2/special_offers/"
    save_dir = get_dir_path('products')
    parser = Parsing5(url, save_dir)
    parser.run()  # запуск парсера

"""