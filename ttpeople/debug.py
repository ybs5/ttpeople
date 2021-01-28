from scrapy import cmdline

"scrapy list|xargs -n 1 scrapy crawl"
cmdline.execute(['scrapy', 'crawl', 'rand'])
