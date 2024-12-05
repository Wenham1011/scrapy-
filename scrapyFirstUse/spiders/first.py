import scrapy
from scrapyFirstUse.items import ScrapyfirstuseItem


class FirstSpider(scrapy.Spider):
    name = "first"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://www.gushiwen.cn/"]
    base_url = "https://www.gushiwen.cn/default_{}.aspx"
    page_index = 1
    def parse(self, response):  # 这里的 response 就是 start_url 请求成功后获取的响应对象
        paragraph_list = response.xpath('/html/body/div[2]/div[1]/div[@class="sons"]')
        for paragraph in paragraph_list:
            title = paragraph.xpath('./div[@class="cont"]/div[starts-with(@id,"zhengwen")]/p[1]//text()').extract_first()
            author = paragraph.xpath('./div[@class="cont"]/div[starts-with(@id,"zhengwen")]/p[2]//text()').extract()
            content = paragraph.xpath('./div[@class="cont"]/div[starts-with(@id,"zhengwen")]/div[@class="contson"]//text()').extract()
            if title and author and content: # 去除none和空
                title_ = title.replace('\n','')
                author_ = ''.join(author).replace('\n','')
                content_ = ''.join(content).replace('\n','')
                # print(title_,author_,content_)

                # 将解析到的数据存储到Item对象
                item = ScrapyfirstuseItem()
                item['title'] = title_  # 访问item对象中的属性无法使用打点 -- item.title
                item['author'] = author_
                item['content'] = content_
                # 提交到管道文件
                yield item

        if self.page_index < 4:    # 结束递归的条件（只爬取前4个页面--经过一些挫折，发现该站只有四页。。。）
            url = self.base_url.format(self.page_index)
            self.page_index += 1
            print("现在开始第{}页的抓取".format(self.page_index))
            # callback参数：请求成功会调用指定的回调函数进行数据解析
            yield scrapy.Request(url, callback=self.parse)



