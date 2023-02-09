import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from multiprocessing import Process, Queue


class MaklatWebsiteSpider(scrapy.Spider):
    name = 'maklat_website'
    allowed_domains = ['www.mklat.com']
    start_urls = [
        'https://www.mklat.com/category/technology/computer-internet']
    custom_settings = {
        'FEEDS': {'scraped_datasets/maklat_website_data.json': {'format': 'json', 'overwrite': True, 'encoding': 'utf8', }}
    }

    def parse(self, response):
        website = response.xpath("//div[@id='logo']/a/@title").get()
        link = response.xpath("//div[@id='logo']/a/@href").get()

        yield {
            "website_name": website,
            "website_link": link,
        }


# To scrape multiple times
def multi_process(q):
    try:
        process = CrawlerRunner()
        p = process.crawl(MaklatWebsiteSpider)
        p.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


# To run the scrape script from the views
def maklatWebsite_scrape():
    q = Queue()
    p = Process(target=multi_process, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result
