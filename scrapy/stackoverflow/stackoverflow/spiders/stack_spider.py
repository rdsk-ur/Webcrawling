import scrapy 
import re

class StackSpider(scrapy.Spider): 
    name = "Stack"
    start_urls = ["https://stackoverflow.com/questions?sort=votes"]
    base_url = "https://stackoverflow.com"
    max_pages = 10
    out_path = "./results.csv"
    output_file = open(out_path, "a")
    # Method to parse the front page, i.e search for searchword
    def parse(self, response):
        tags = response.xpath('//a[@class="post-tag"]/text()').extract()
        for tag in tags:
            self.output_file.write(tag + "\n")


        current_page = int(response.xpath('//a[@class="page-numbers current"]/text()')[0].extract())
        #get to next page if not max_pages visited
        if current_page < self.max_pages:
            next_page = response.xpath(
                '//a[./span[@class="page-numbers" and contains(text(),{})]]/@href'.format(
                    current_page + 1
                )).extract()
            if next_page is not None:
                yield scrapy.Request(self.base_url+next_page, callback=self.parse)

        else:
            self.output_file.flush()
            self.output_file.close()
            self.plot_tags(self.out_path)