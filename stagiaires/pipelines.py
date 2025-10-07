# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LinkedinPipeline:
    def process_item(self, item, spider):
        return item

# pipelines.py
import json

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('stages.json', 'w', encoding='utf-8')
        self.file.write("[\n")  # start JSON array
        self.first_item = True

    def close_spider(self, spider):
        self.file.write("\n]")
        self.file.close()

    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(",\n")
        self.first_item = False
        json.dump(item, self.file, ensure_ascii=False, indent=4)
        return item
