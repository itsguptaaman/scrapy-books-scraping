
from pathlib import Path
import scrapy
import json


data = []

def write_to_json(data, page_category):
    with open(f'{page_category}.json', 'w') as f:
        json.dump({page_category: data}, f)

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def start_requests(self):
        urls = [
            "http://books.toscrape.com/catalogue/category/books/science_22/index.html",
            "http://books.toscrape.com/catalogue/category/books/fiction_10/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"
        booksdetail = {}
        # Save the content as file
        # Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        cards = response.css(".product_pod")
        for card in cards:
            title = card.css("h3>a::text").get()
            print(title)

            rating = card.css(".star-rating").attrib["class"].split(" ")[1]
            print(rating)

            image = card.css(".image_container img")
            print(image.attrib["src"])

            price = card.css(".price_color::text").get()
            print(price)

            availability = card.css("availability")
            if len(availability.css(".icon-ok")) > 0:
                in_stock = True
            else:
                in_stock = False
                
            data.append({"title": title, "rating": rating, "image": image, "price": price, "in_stock": in_stock})

        write_to_json(data, page)