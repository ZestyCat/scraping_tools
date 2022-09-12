import scrapy
import csv
from w3lib import html
import re

def clean_text(text):
    clean = re.sub(r"(\n)+", " ", html.remove_tags(text))
    return clean

class BlogSpider(scrapy.Spider):
    name = "posts"

    def start_requests(self):
        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; rv:104.0) Gecko/20100101 Firefox/104.0"}
        blog_url = "https://www.becomingminimalist.com/"
        pages = 10
        for page in range(0, pages):
            if page == 0:
                url = blog_url 
            else:
                ext = f"page/{page}"
                url = blog_url + ext
            yield scrapy.Request(url=url, headers=headers, callback=self.get_pages)

    def get_pages(self, response):
        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; rv:104.0) Gecko/20100101 Firefox/104.0"}
        links = response.css("a.entry-title-link::attr(href)").getall()
        for link in links:
            yield scrapy.Request(url=link, headers=headers, callback=self.parse)

    def parse(self, response):
        title = response.css("h1.entry-title").get()
        author = response.css("span.entry-author-name").get()
        post_url = response.url
        n_comments = response.css("span.entry-comments-link a::text").get() \
                .split(" ")[0]
        content = clean_text(" ".join(response.css("div.entry-content p").getall()))
        with open("becomingminimalist_blog_posts.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow([title, author, post_url, n_comments, content])

