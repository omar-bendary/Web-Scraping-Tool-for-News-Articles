import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from multiprocessing import Process, Queue


class ArabMediaSocietyArticlesSpider(scrapy.Spider):
    name = 'arab_media_society_articles'
    allowed_domains = ['www.arabmediasociety.com']
    start_urls = ['https://www.arabmediasociety.com/category/features']
    custom_settings = {
        'FEEDS': {'scraped_datasets/arab_media_society_articles_data.json': {'format': 'json', 'overwrite': True, 'encoding': 'utf8', }}
    }

    def parse(self, response):
        website = response.xpath("//div[@class='logo']/h2/a/@title").get()
        articles = response.xpath(
            "//div[@class='post-listing archive-box']/article")

        for article in articles:
            title = article.xpath(
                ".//h2[@class='post-box-title']/a/text()").get()
            link = article.xpath(
                ".//h2[@class='post-box-title']/a/@href").get()
            description = article.xpath(
                ".//div[@class='entry']/p/text()").get()

            yield response.follow(url=link, callback=self.parse_article, meta={'website_name': website, 'article_title': title, 'article_link': link, 'article_description': description})

        next_page = response.xpath(
            "//span[@id='tie-next-page']/a/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response):
        website = response.request.meta['website_name']
        title = response.request.meta['article_title']
        link = response.request.meta['article_link']
        description = response.request.meta['article_description']
        DOM = response.xpath(
            "//article[@id='the-post']").get().split('<div')[0]
        published_at = response.xpath("//span[@class='tie-date']/text()").get()

        yield {
            'website_name': website,
            'article_title': title,
            'article_link': link,
            'article_description': description,
            'article_DOM': DOM,
            'article_published_at': published_at

        }


# To scrape multiple times
def multi_process(q):
    try:
        process = CrawlerRunner()
        p = process.crawl(ArabMediaSocietyArticlesSpider)
        p.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


# To run the scrape script from the views
def arab_media_society_scrape():
    q = Queue()
    p = Process(target=multi_process, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result
