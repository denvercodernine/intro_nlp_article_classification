from scrapy.item import Item, Field

class VNExpressItem(Item):
    # define the fields for your item here like:
    title = Field()
    description = Field()
    url = Field()
    content = Field()
    writtenOn = Field()
    tags = Field()
    catid = Field()
    postid = Field()