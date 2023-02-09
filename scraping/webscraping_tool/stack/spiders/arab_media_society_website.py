import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from multiprocessing import Process, Queue


class ArabMediaSocietyWebsiteSpider(scrapy.Spider):
    name = 'arab_media_society_website'
    allowed_domains = ['www.arabmediasociety.com']
    start_urls = ['https://www.arabmediasociety.com/category/features']
    custom_settings = {
        'FEEDS': {'scraped_datasets/arab_media_society_website_data.json': {'format': 'json', 'overwrite': True, 'encoding': 'utf8', }}
    }

    def parse(self, response):
        website = response.xpath("//div[@class='logo']/h2/a/@title").get()
        link = response.xpath("//div[@class='logo']/h2/a/@href").get()

        yield {
            "website_name": website,
            "website_link": link,
        }


# To scrape multiple times
def multi_process(q):
    try:
        process = CrawlerRunner()
        p = process.crawl(ArabMediaSocietyWebsiteSpider)
        p.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


# To run the scrape script from the views
def arab_media_society_website_scrape():
    q = Queue()
    p = Process(target=multi_process, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result
