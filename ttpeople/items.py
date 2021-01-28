# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TtpeopleItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    job = scrapy.Field()
    birthday = scrapy.Field()
    prev_job = scrapy.Field()
    place = scrapy.Field()
    education = scrapy.Field()
    introduce = scrapy.Field()
    research_focus = scrapy.Field()
    awards = scrapy.Field()
    recent_projects = scrapy.Field()
    tags = scrapy.Field()
    languages = scrapy.Field()
    profile_photo = scrapy.Field()
    source = scrapy.Field()
    social_account = scrapy.Field()
    url = scrapy.Field()
    created_time = scrapy.Field()
