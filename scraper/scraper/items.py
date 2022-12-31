import scrapy 

class SrealityItem(scrapy.Item):
    title = scrapy.Field()
    image_url = scrapy.Field()