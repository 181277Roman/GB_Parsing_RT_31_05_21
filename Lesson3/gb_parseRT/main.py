from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from gb_parse.spiders.youla import AutoyoulaSpider
from gb_parse.spider.hh import HhRemoteSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule("gb_parse.settings")
    crowler_process = CrawlerProcess(settings=crawler_settings)
    crowler_process.crawl(AutoyoulaSpider)
    crowler_process.crawl(HhRemoteSpider)
    crowler_process.start()





""""# Don`t forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .settings import BOT_NAME
from pymongo import MongoClient


class GbParsePipeLine:

    def process_item(self, item, spider):
        return item

class GbMongoPipeLine:

    def __init__(self):
        client = MongoClient()
        self.db = client[BOT_NAME]

    def process_item(self, item, spider):
        collection_name = f"{spider.name}_{item.get('item_type', '')}"
        self.db[collection_name].insert_one(item)
        return item

"""