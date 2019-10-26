# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class WikipediaItem(scrapy.Item):
	title = scrapy.Field()
	content = scrapy.Field()
	url = scrapy.Field()
	def __str__(self):
		return self['url']