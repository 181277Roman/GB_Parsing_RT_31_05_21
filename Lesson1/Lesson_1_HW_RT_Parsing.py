from pathlib import Path
import requests
import time
import json

"""  url = "https://5ka.ru/special_offers/?store=310D/"

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

"""


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
