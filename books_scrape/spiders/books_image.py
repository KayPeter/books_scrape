import scrapy


class BooksImageSpider(scrapy.Spider):
    name = 'books_image'
    # allowed_domains = ['www.books.toscrape.com']
    start_urls = ['https://books.toscrape.com']

    def parse(self, response):
        for book in response.xpath("//div[@class='image_container']/a/@href").getall():
            yield response.follow(book, callback=self.parse_book)
        
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(response.urljoin(next_page))

    def parse_book(self, response):
        img_links=[]
        for img in response.xpath("//div[@class='thumbnail']//img/@src").getall():
            img_links.append(response.urljoin(img))
            
        yield {
            'title': response.xpath('//h1/text()').get(),
            'price': response.xpath("//p[@class='price_color']/text()").get(),
            'image_urls': img_links,
        }
