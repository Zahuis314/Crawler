# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import spacy
from unicodedata import normalize
from collections import OrderedDict
import math


def split(item):
	chunks = int(math.ceil(len(item)/100))
	for i in range(chunks):
		yield item[i*100:(i*100)+100]
def is_valid_token(token):
	return not token.is_punct and not token.is_digit and not token.is_space and token.is_alpha

class WikipediaPipeline(object):
	count=0
	def __init__(self, *args, **kwargs):
		self.nlp = spacy.load('es_core_news_md')
		# self.vocabulary = OrderedDict()
		self.vocabulary = set()
	def process_item(self, item, spider):
		self.url_file.write("%s\n"%item['url'])
		if item:
			WikipediaPipeline.count = 1 + WikipediaPipeline.count
			print("%d - %s"%(WikipediaPipeline.count,item['url']))
			# print(item['title'])
			doc = self.nlp(item['content'])
			tokens_valid = [normalize('NFC',token.text.lower()).encode('utf-8') for token in doc if is_valid_token(token)]
			for tok in tokens_valid:
				self.vocabulary.add(tok)
			for piece in split(tokens_valid):
				self.data_file.write("%s;%s\n"%(item['url']," ".join(piece)))
		return item
	def open_spider(self, spider):
		self.url_file = open('url.txt', 'w')
		self.data_file = open('items.csv', 'w')
		self.vocabulary_file = open('vocabulary.txt', 'w')
	def close_spider(self, spider):
		for word in self.vocabulary:#.keys():
			self.vocabulary_file.write("%s\n"%word)
		self.data_file.close()
		self.vocabulary_file.close()
		self.url_file.close()