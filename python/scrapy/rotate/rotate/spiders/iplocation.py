import scrapy

class IpLocation(scrapy.Spider):
    name = "iplocation"

    start_urls = ["https://flask.palletsprojects.com/en/2.2.x/"]

    def parse(self, response):
        h = response.css("h2::text").get()
        print(h)
