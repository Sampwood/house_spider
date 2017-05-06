## 基于Scrapy的python爬虫

爬取房价信息

## 启动项目：scrapy crawl dmoz

## 小tips

> spider返回item之后，在settings.py里面设置ITEM_PIPELINES才有用
> spider的parse_start_url方法是对start_urls的处理
> python控制台是用gbk（操作系统编码方式？）编码的，获取的网页数据是unicode编码的