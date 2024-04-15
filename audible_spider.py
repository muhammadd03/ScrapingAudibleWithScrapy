############################################################################################################
# There are three ways to change the user agent
# 1 change the user agent variable in settings.py file
# 2 User agent to the defaul request header in the settings.py file
# 3 make a def start_request function and add the user agent in the header
############################################################################################################
import scrapy


class AudibleSpiderSpider(scrapy.Spider):
    name = "audible_spider"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]

    def start_requests(self):
        yield scrapy.Request(url='https://www.audible.com/search', callback=self.parse,
                       headers={
                           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
                       })


    def parse(self, response):
        product_container = response.xpath('//div[@class="adbl-impression-container "]/div/span/ul/li')

        for product in product_container:
            book_title = product.xpath('.//h3[contains(@class, "bc-heading")]/a/text()').get()
            book_author = product.xpath('.//li[contains(@class, "authorLabel")]/span/a/text()').getall()
            book_lenght = product.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get()

            yield {
                'title': book_title,
                'author': book_author,
                'lenght': book_lenght,
                'User-Agent':response.request.headers['User-Agent']
            }

            pagination = response.xpath('//ul[contains(@class, "pagingElements")]')
            next_page_url = pagination.xpath('.//span[contains(@class, "nextButton")]/a/@href').get()

            if next_page_url:
                yield response.follow(url=next_page_url, callback=self.parse, headers={
                           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
                       })
