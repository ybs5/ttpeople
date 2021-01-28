import json
import scrapy
from ttpeople.common import utils
from ttpeople.items import TtpeopleItem


class RandSpider(scrapy.Spider):
    name = 'rand'
    allowed_domains = ['rand.org']
    start_urls = ['https://www.rand.org/content/rand/about/people/_jcr_content/par/stafflist.xml']

    def parse(self, response):
        for el in response.xpath('//stafflist/staff'):
            name = el.css('::attr(slug)').get()
            meta = {'detail_url': f'https://www.rand.org/about/people/{name[0]}/{name}.html'}
            contact_url = f'https://www.rand.org/about/people/{name[0]}/{name}/_jcr_content/par/bio.contact.json'
            yield scrapy.http.JsonRequest(contact_url, callback=self.parse_contact, meta=meta, dont_filter=True)

    def parse_contact(self, response):
        contact = json.loads(response.text)
        url = response.meta['detail_url']
        yield scrapy.Request(url, callback=self.parse_detail, meta=contact, dont_filter=True)

    @staticmethod
    def parse_detail(response):
        languages = response.css('.languages::text').extract()
        social_account = {}
        for li in response.css('.bio-meta ul.icon-list li'):
            name = li.css('a::attr(class)').get()
            if not name: continue
            social_account[name] = li.css('a::attr(href)').get()

        _ = utils.get_clearfix_text
        yield TtpeopleItem(
            name=response.css('#RANDTitleHeadingId::text').get(),
            job=response.css('.basic-info .title::text').get(),
            email=response.meta.get('email'),
            phone=response.meta.get('phone'),
            prev_job=_(response.css('.previous_positions::text').extract(), add_root=True),

            place=response.css('.basic-info .locality::text').get(),
            education=response.css('.education p::text').get(),
            introduce=_(response.css('.biography p').extract(), add_root=True),
            research_focus=response.css('ul.related-topics a::text').extract(),
            awards=response.css('.honors ul li::text').extract(),

            recent_projects=response.css('.recent_projects ul li::text').extract(),
            languages=''.join(languages).strip().split(';'),
            profile_photo=response.css('.basic-info img.photo::attr(src)').get(),
            social_account=social_account,
            url=response.url
        )
