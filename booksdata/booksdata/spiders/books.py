import scrapy
from pathlib import Path
import json


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]

    # Use 'start_requests' instead of 'start'
    def start_requests(self):
        self.data =[]
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            # We yield a Request, which is a standard generator action
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        books = response.css(".product_pod")

        for book in books:
            self.data.append({
                "title": book.css("h3 a::attr(title)").get(),
                "link": response.urljoin(book.css("h3 a::attr(href)").get())
            })

    def closed(self, reason):
        import pandas as pd
        df = pd.DataFrame(self.data)
        print(df.head())
        df.to_excel("books.xlsx", index=False)
#two files will be created in the same directory where the spider is run, one for each category of books (travel and mystery). Each file will contain the HTML content of the respective page.