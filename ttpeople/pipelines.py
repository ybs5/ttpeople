# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
from ttpeople.db import Es


class TtpeoplePipeline:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            use_es=crawler.settings.get('ES_HOST', '') != "",
            use_kafka=crawler.settings.get('KAFKA_URL', '') != "",
        )

    def __init__(self, use_es=True, use_kafka=True):
        self.use_es = use_es
        self.use_kafka = use_kafka

    def process_item(self, item, spider):  # noqa
        for str_field in ['name', 'email', 'phone', 'job', 'birthday', 'prev_job', 'place', 'education',
                          'introduce', 'profile_photo']:
            item[str_field] = (item.get(str_field) or '').strip()

        for list_field in ['research_focus', 'awards', 'recent_projects', 'tags', 'languages']:
            data_list = item.get(list_field) or []
            item[list_field] = [str(dl).strip() for dl in data_list if str(dl).strip()]

        item['source'] = spider.name
        item['social_account'] = item.get('social_account') or {}
        item['created_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.use_es:
            es = Es()
            es.save(dict(item))
        return item
