import scrapy
from scraper.items import VNExpressItem
from datetime import datetime, time
import logging
import re

cat_ids = {1001005: "Thời sự", 1001002: "Thế giới", 1003159: "Kinh doanh", 1002691: "Giải trí", 1002565: "Thể thao",
           1001007: "Pháp luật", 1003497: "Giáo dục", 1003750: "Sức khỏe", 1002966: "Đời sống", 1003231: "Du lịch", 1001009: "Khoa học"}

punctuation = [r'!',  r'&',
               r'(', r')', r'*', r'+', r',', u':', u';', u'=', u'>', u'?', u'.']


def clean_text(text):
    for punc in punctuation:
        text = text.replace(punc, ' ')
    text = text.replace('VnExpress', '')
    return text  # .lower()


midnight = datetime.combine(datetime.today(), time.min)
timestamp_midnight = int(datetime.timestamp(midnight))

# history = date.fromisoformat('2010-01-01')
timestamp_history = 1262304000  # 1604188800


class VNExpressSpider(scrapy.Spider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]

    def start_requests(self):
        urls = []
        for id in cat_ids:
            urls.append(
                f"https://vnexpress.net/category/day?cateid={id}&fromdate={timestamp_history}&todate={timestamp_midnight}&allcate={id}")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_category_page)

    def parse_category_page(self, response):
        cat = cat_ids[int(response.url.split(
            '/')[-1].split('&')[0].split('=')[-1])]

        logging.info(f'Category: {cat}')

        base_selector = response.xpath('//h3[@class="title-news"]')
        for sel in base_selector:
            link = sel.xpath('./a/@href').extract()
            link_text = sel.xpath('./a/text()').extract()
            # clean the data
            link = link[0] if link else 'n/a'
            link_text = link_text[0].strip() if link else 'n/a'
            logging.info(f"Link: {link}\nTitle: {link_text}")
            yield response.follow(url=link, callback=self.parse_article_page)


        #Limiting the amount of articles scraped for now
        next_page = response.xpath(
            "//a[@class='btn-page next-page ']/@href").extract()

        if len(next_page) > 0:
            yield response.follow(url=next_page[0], callback=self.parse_category_page)


    def parse_article_page(self, response):

        post_content = response.xpath(
            './/p[@class="Normal"]/text()').getall()
        post_time = response.xpath(
            './/span[@class="date"]/text()').getall()
        post_tags = response.xpath(
            './/h4[@class="item-tag"]/a/@title').getall()
        cat_id = response.xpath(
            './/meta[@name="tt_category_id"][1]/@content').getall()
        post_id = response.xpath(
            './/meta[@name="tt_article_id"][1]/@content').getall()
        post_title = response.xpath(
            './/meta[@itemprop="headline"]/@content').getall()
        post_url = response.xpath(
            './/meta[@property="og:url"]/@content').getall()
        description = response.xpath(
            './/meta[@name="description"]/@content').getall()
        cat_id_list = response.xpath(
            './/meta[@name="tt_list_folder"][1]/@content').getall()
        cat_id_base = response.xpath(
            './/meta[@name="tt_site_id_new"][1]/@content').getall()
        text = re.sub('\n', ' ', ''.join(post_content))
        if len(text) < 100:
            return
        item = VNExpressItem()
        item['title'] = post_title
        item['description'] = clean_text(description[0])
        item['url'] = post_url
        item['content'] = clean_text(text)
        item['writtenOn'] = post_time
        item['tags'] = post_tags
        item['catid'] = cat_id
        item['postid'] = post_id
        item['catidlist'] = cat_id_list
        item['catidbase'] = cat_id_base

        yield item
