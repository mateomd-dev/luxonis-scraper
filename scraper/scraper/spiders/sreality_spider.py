import scrapy
from scraper.items import SrealityItem
from scrapy_playwright.page import PageMethod

class SrealitySpider(scrapy.Spider):
    name = 'sreality_spider'
    start_url = 'https://www.sreality.cz/hledani/prodej/byty'

    def start_requests(self):
        yield scrapy.Request(self.start_url, 
            meta=dict (
                playwright = True,
                playwright_include_page = True,
                playwright_page_coroutines = [
                    PageMethod('wait_for_selector', '.dir-property-list')
                ]
            ))

    async def parse(self, response):
        for item in response.css("div.property"):
            title = item.css('span.name.ng-binding::text').get()
            image_url = item.css('img::attr(src)').get()

            sreality_item = SrealityItem()
            sreality_item["title"] = title
            sreality_item["image_url"] = image_url

            yield sreality_item

        next_page = response.css('a.paging-next::attr(href)').get()
        next_page = self.start_url + "?strana=" + next_page.split("?strana=")[1]
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse,  meta=dict (
                playwright = True,
                playwright_include_page = True,
                playwright_page_coroutines = [
                    PageMethod('wait_for_selector', '.dir-property-list')
                ]
            ))
