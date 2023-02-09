import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from multiprocessing import Process, Queue


class MaklatArticlesSpider(scrapy.Spider):
    name = 'maklat_articles'
    allowed_domains = ['www.mklat.com']
    start_urls = [
        'https://www.mklat.com/category/technology/computer-internet']
    custom_settings = {
        'FEEDS': {'scraped_datasets/maklat_articles_data.json': {'format': 'json', 'overwrite': True, 'encoding': 'utf8', }}
    }

    def parse(self, response):
        website = response.xpath("//div[@id='logo']/a/@title").get()
        articles = response.xpath("//ul[@id='posts-container']/li")

        for article in articles:
            title = article.xpath(".//h2[@class='post-title']/a/text()").get()
            link = article.xpath(".//h2[@class='post-title']/a/@href").get()
            description = article.xpath(
                ".//div[@class='post-details']/p/text()").get()

            yield response.follow(url=link, callback=self.parse_article, meta={'website_name': website, 'article_title': title, 'article_link': link, 'article_description': description})

        next_page = response.xpath(
            "//li[@class='the-next-page']/a/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response):
        website = response.request.meta['website_name']
        title = response.request.meta['article_title']
        link = response.request.meta['article_link']
        description = response.request.meta['article_description']
        DOM = response.xpath("//article[@id='the-post']").re_first('.+')

        yield {
            'website_name': website,
            'article_title': title,
            'article_link': link,
            'article_description': description,
            'article_DOM': DOM,
            'article_published_at': None
        }


# To scrape multiple times
def multi_process(q):
    try:
        process = CrawlerRunner()
        p = process.crawl(MaklatArticlesSpider)
        p.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


# To run the scrape script from the views
def maklatArticles_scrape():
    q = Queue()
    p = Process(target=multi_process, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result
