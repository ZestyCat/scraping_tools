import scrapy
import numpy as np
import csv
import re
import json

def clean_text(text, re_sub = (r"", r"")):
    """ Remove html tags, hashtags, email address, urls, slashes, special chars, double periods 
        Use re_sub param to pass extra params to re.sub before text cleaning
    """
    cleaned = \
        re.sub(r"(\s+)|(\n)", " ",
        re.sub(r"(\.\.)|(\.\s+){2,}", ". ", 
        re.sub(r"([^a-zA-z0-9\s\-\.#])","",
        re.sub(r"/", " ", 
        re.sub(r"(\s#\S+)|(\S+@\S+\.\S{3})|(https{0,1}://\S+)|(\S{3}\.\S+\.\S{3}\.\S+)|(\S+\.com)|([\[\]])", " ",
        re.sub(r"(<.*?>)+", r". ",
        re.sub(re_sub[0], re_sub[1], text)))))))
    return cleaned

class BoozSpider(scrapy.Spider):
    name = "boozjobs"

    def start_requests(self, n_jobs = 20):        
        for j in np.arange(0, n_jobs, 10):
            if j == 0:
                continue
            url = 'https://careers.boozallen.com/jobs/search/?jobOffset={}'.format(int(j))
            yield scrapy.Request(url=url, callback=self.get_links)

    def get_links(self, response):
        for link in response.css("a.link::attr(href)").getall():
            yield scrapy.Request(url=link, callback=self.get_page)

    def get_page(self, response):
        job = re.sub(r"[^a-zA-z0-9\s\-]"," ",response.css("title::text").get().strip())
        description = clean_text(response.css("div.article__content--rich-text").get(), re_sub=(r"(</{0,1}span?>)+", ""))
        with open ("jobs.csv", "a") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(["Booz Allen Hamilton", job, description])
            print(description)

class NorthropSpider(scrapy.Spider):
    name = "northropjobs"

    def start_requests(self, n_pages = 3):        
        for j in range(1, n_pages):
            url = 'https://www.northropgrumman.com/jobs/page/{}/'.format(int(j))
            yield scrapy.Request(url=url, callback=self.get_links)

    def get_links(self, response):
        used_links = [] # Duplicate links to skip
        for link in response.css("a::attr(href)").getall():
            if "jobs" in link and "page" not in link and link not in used_links:
                print(link)
                used_links.append(link)
                yield scrapy.Request(url=link, callback=self.get_page)

    def get_page(self, response):
        job = re.sub(r"[^a-zA-z0-9\s\-]"," ",response.css("title::text").get())
        description = clean_text(response.css("div.jobContent").get())

        with open("jobs.csv", "a") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(["Northrop Grumman", job, description])
            print(description)

class MontroseScraper(scrapy.Spider):
    name = "montrosejobs"

    with open("./montrose_listings.json") as f:
        jobs = json.loads(f.read())
        urls = [job["externalPath"] for job in jobs["jobPostings"]]

    def start_requests(self, urls = urls):
        base_url = "https://montrose.wd1.myworkdayjobs.com/wday/cxs/montrose/MEG"
        for url in urls:
            yield scrapy.Request(url=base_url+url, callback=self.get_page)

    def get_page(self, response):
        job = re.sub(r"[^a-zA-z0-9\s\-]"," ",response.json()["jobPostingInfo"]["title"])
        description = clean_text(response.json()["jobPostingInfo"]["jobDescription"])
        with open("jobs.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(["Montrose", job, description])
            print(job)

class AmazonSpider(scrapy.Spider):
    name = "amazonjobs"
    
    def start_requests(self, n_jobs = 5000):
        for offset in np.arange(0, n_jobs, 100):
            url = f"https://www.amazon.jobs/en/search.json?radius=5000km&facets[]=normalized_country_code&facets[]=normalized_state_name&facets[]=normalized_city_name&facets[]=location&facets[]=business_category&facets[]=category&facets[]=schedule_type_id&facets[]=employee_class&facets[]=normalized_location&facets[]=job_function_id&facets[]=is_manager&facets[]=is_intern&offset={offset}&result_limit=100sort=relevant&latitude=&longitude=&loc_group_id=&loc_query=&base_query=&city=&country=USA&region=&county=&query_options=&category[]=software-development&"
            yield scrapy.Request(url=url, callback=self.get_data)

    def get_data(self, response):
        for job in response.json()["jobs"]:
            title = re.sub(r"[^a-zA-z0-9\s\-]"," ",job["title"])
            # remove tags, slashes, hashtags, emails, urls, special chars, finally double periods
            qualifications = clean_text(job["preferred_qualifications"])
            with open("jobs.csv", "a") as file:
                writer = csv.writer(file)
                writer.writerow(["Amazon", title, qualifications])
