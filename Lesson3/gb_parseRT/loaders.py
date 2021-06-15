from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from scrapy import Selector
from itemloaders.processors import TakeFirst, MapCompose

def clear_price(price:str):
    try:
        result = float(price.replace("\u2000", ""))
    except ValueError:
        result = None
    return result

def get_characteristics(item: str):
    selector = Selector(text=item)
    data = {
        "name": selector.xpath("//div[contains(@class, 'AdvertSpecs_label')]/text()").get(),
        "value": selector.xpath("//div[contains(@class, 'AdvertSpecs_data')]/text()").get()
    }
    return data

def create_author_link(author_id: str):
    author = ""
    if author_id:
        author = urljoin("https://youla.ru/user/", author_id)
    return author


#def take_first(items: list):
    #return items[0]  # при использовании itemloaders.processor эта часть кода не нужна

class AutoyolaLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    price_in = MapCompose(clear_price)
    price_out = TakeFirst()
    description_out = TakeFirst()
    characteristics = MapCompose(get_characteristics)
    author_in = MapCompose(create_author_link)
    author_out = TakeFirst()


