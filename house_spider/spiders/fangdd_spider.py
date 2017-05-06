import scrapy
import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from house_spider.items import FangddItem

# =======================================================================================================0
class houseSpider(CrawlSpider):
    name = "fangdd"
    allowed_domains = ["fangdd.com"]
    start_urls = ["http://www.fangdd.com/hangzhou"]
    i = 0
    linkList = []

    path = "resources/"
    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        # Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),
        # Rule(LinkExtractor(allow=('xf.*hangzhou', ))),
        # 提取匹配 'hangzhou' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('xf.*hangzhou/[0-9]*\.html', )), callback='parse_item', follow=True),	
    )

    def parse_item(self, response):
    	print(self.i)
    	print(response.url)
    	# print(response.status)
    	# print(response.headers)
    	# print(response.request)
    	# print(response.meta)
    	# print(response.flags)
        filename = "fangdd.html"
        link = response.url.split("/")[4].split(".")[0]
        if link not in self.linkList:
        	self.i += 1
        	self.linkList.append(link)
	        with open(self.path + filename, 'ab') as f:
	            f.write(response.url+ "\n")

# =======================================================================================================1
class house1Spider(CrawlSpider):
    name = "fangdd1"
    allowed_domains = ["fangdd.com"]
    start_urls = ["http://xf.fangdd.com/hangzhou/loupan/pg1"]

    path = "resources/"
    rules = (
        Rule(LinkExtractor(allow=('/loupan'), restrict_xpaths=('//a[@class="next"]')), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=('/loupan'), restrict_xpaths=('//div[@class="xf-step"]/a')), callback='parse_item2', follow=False),
        Rule(LinkExtractor(allow=('51762\.html', )), callback='parse_item3', follow=False),
    )

    def parse_item(self, response):
    	print("------------------------------------")
    	print(response.url)
    	print("------------------------------------")

    def parse_item2(self, response):
    	print("====================================")
    	print(response.url)
    	print("====================================")
    	return Request(url="http://xf.fangdd.com/hangzhou/51762.html")

    def parse_item3(self, response):
    	print("************************************")
    	print(response.url)
    	print("************************************")

# =======================================================================================================2
class house2Spider(CrawlSpider):
    name = "fangdd2"
    allowed_domains = ["fangdd.com"]
    start_urls = ["http://www.fangdd.com/hangzhou"]

    path = "resources/"
    rules = (
        Rule(LinkExtractor(allow=('xf.*hangzhou/[0-9]*\.html$', )), callback='parse_item', follow=True),	
    )

    def parse_item(self, response):
    	item = FangddItem()
    	item['link'] = response.url
    	yield item

# =======================================================================================================3
class house3Spider(CrawlSpider):
    name = "fangdd3"
    allowed_domains = ["fangdd.com"]
    start_urls = ["http://xf.fangdd.com/hangzhou/loupan/pg1"]
    i = 0

    path = "resources/"
    rules = (
        Rule(LinkExtractor(allow=('/loupan'), restrict_xpaths=('//a[@class="next"]')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
    	logging.warning(self.i)
    	logging.warning(response.url)
    	self.i += 1
        filename = "fangdd1.html"
        with open(self.path + filename, 'ab') as f:
        	for i, val in enumerate(response.css('li span.hsname::text').extract()) :
                	f.write(val.encode('utf-8') + "-"+ 
             		response.css('li span.hsname+a::attr(data-house-id)').extract()[0].encode('utf-8') + "\n")

    def parse_start_url(self, response):
    	self.parse_item(response)
        return []

# =======================================================================================================4
class house4Spider(CrawlSpider):
    name = "fangdd4"
    allowed_domains = ["fangdd.com"]
    start_urls = ["http://xf.fangdd.com/hangzhou/loupan/pg1"]
    i = 0

    path = "resources/"
    rules = (
        Rule(LinkExtractor(allow=('/loupan'), restrict_xpaths=('//a[@class="next"]')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
    	logging.warning(self.i)
    	logging.warning(response.url)
    	self.i += 1
        filename = "fangdd1.html"
        with open(self.path + filename, "ab") as f:
        	for house in response.css("ul.house-list>li"):
        		hsname = house.css("span.hsname::text").extract()
        		hsid = house.css("a.comment::attr(data-house-id)").extract()
        		print(hsname[0].encode('utf-8'))
        		f.write(hsname[0].encode('utf-8') + "-" + hsid[0].encode('utf-8') + "\n")

    def parse_start_url(self, response):
    	print("====================================")
    	print(response)
    	self.parse_item(response)
    	print("====================================")
        return []

# =======================================================================================================5
class house5Spider(CrawlSpider):
    name = "fangdd5"
    allowed_domains = ["fangdd.com"]
    start_urls = ["http://xf.fangdd.com/hangzhou/loupan/pg1"]
    i = 0 

    rules = (
        Rule(LinkExtractor(allow=('/loupan'), restrict_xpaths=('//a[@class="next"]')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
    	p = 0
    	item = FangddItem()
    	self.i += 1
    	print(self.i)
    	for house in response.css("ul.house-list>li"):
    		p += 1
    		print(p)
    		item["name"] = house.css("span.hsname::text").extract()[0]
    		item["link"] = house.css("a.comment::attr(data-house-id)").extract()[0]
    		yield item

    def parse_start_url(self, response):
    	item = FangddItem()
    	item = self.parse_item(response)
    	return item

# =======================================================================================================6
class house6Spider(CrawlSpider):
    name = "fangdd6"
    allowed_domains = ["fangdd.com"]
    start_urls = ["http://xf.fangdd.com/hangzhou/loupan/pg1"]

    rules = (
        Rule(LinkExtractor(allow=('/loupan'), restrict_xpaths=('//a[@class="next"]')), callback='parse_link', follow=True),
    )

    def parse_start_url(self, response):
    	self.parse_link(response)
    	return []

    def parse_link(self, response):
    	for house in response.css("ul.house-list>li"):
    		link = house.css("a.comment::attr(data-house-id)").extract()[0]
    		url = "http://xf.fangdd.com/hangzhou/" + link + ".html"
    		yield Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
    	with open("resources/fangdd2.html", "ab") as f:
    		f.write(response.url+ "\n")

# =======================================================================================================7
class house7Spider(CrawlSpider):
    name = "fangdd7"
    allowed_domains = ["fangdd.com"]
    start_urls = ["http://xf.fangdd.com/hangzhou/loupan/pg1"]

    rules = (
        Rule(LinkExtractor(allow=('/loupan'), restrict_xpaths=('//a[@class="next"]')), callback='parse_link', follow=True),
    )

    def parse_start_url(self, response):
    	self.parse_link(response)
    	return []

    def parse_link(self, response):
    	for house in response.css("ul.house-list>li"):
    		link = house.css("a.comment::attr(data-house-id)").extract()[0]
    		url = "http://xf.fangdd.com/hangzhou/" + link + ".html"
    		yield Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
    	item = FangddItem()
    	item["link"] = response.url.split("/")[4].split(".")[0]
    	item["name"] = response.css("h1.hs-name::text").extract()[0]
    	item["price"] = response.css("div.average big::text").extract()[0]
    	item["address"] = response.css("div.infor span.address::text").extract()[0]
    	time = response.css("div.hs-infor div.infor p:nth-child(3)::text").extract()
    	item["time_open"] = time[0].split(u'\uff1a')[1].strip()
    	item["time_end"] = time[1].split(u'\uff1a')[1].strip()
    	item["style"] = response.css("div.hs-infor div.infor p:first-child::text").extract()[0].split(u'\uff1a')[1].strip().replace(u'\r\n', "").replace(" ", "")
    	item['decoration'] = response.css("table.building-table tr:nth-child(3) td:nth-child(2)::text").extract()[0].strip().replace(u'\r\n', "").replace(" ", "")
    	yield item
