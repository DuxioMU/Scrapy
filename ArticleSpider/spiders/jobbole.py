# -*- coding: utf-8 -*-
import scrapy
import datetime
import re

from ArticleSpider.utils.common import get_md5
from ArticleSpider.items import JobBoleArticleItem

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/113499/', 'http://blog.jobbole.com/113576/']

    def parse(self, response):
        article_item = JobBoleArticleItem()

        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #         f.write(response.body)
        front_image_url = response.meta.get("front_image_url", "")
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        create_date = response.xpath('///p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace("·", "").strip()
        praise_nums = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract()[0]
        fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)

        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)

        content = response.xpath("//div[@class='entry']").extract()[0]

        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        article_item["url_object_id"] = get_md5(response.url)
        article_item["title"] = title
        article_item["url"] = response.url
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item["create_date"] = create_date
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comment_nums
        article_item["fav_nums"] = fav_nums
        article_item["tags"] = tags
        article_item["content"] = content


