#!/usr/bin/env python
# coding: utf-8

from collections import OrderedDict
import scrapy
from bs4 import BeautifulSoup       
from wikipedia.items import WikipediaItem
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.utils.httpobj import urlparse_cached
import urlparse
import json
from unicodedata import normalize
class Queue:
    def __init__(self, max_visit):
        self.store = OrderedDict()
        self.visited = set()
        self.max_visit = max_visit
        self.current=0
    @property
    def can_visit(self):
        return len(self.visited) < self.max_visit
 
    def pop(self):
        item = self.store.popitem(False)
        if len(self.visited) < self.max_visit:
            return item[0]
        return None
    def duplicated(self, item):
        parsed = urlparse.urlparse(item)
        return ("%s://%s%s/%s/%s"%(parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query)) in self.visited
    def push(self, item):
        if (not self.duplicated(item)) and (item not in self.visited) and (not self.store.has_key(item)) and self.current < self.max_visit and urlparse.urlparse(item).hostname in WikipediaSpider.allowed_domains:
            self.current+=1
            self.store[item]=self.current

    def visit(self,item):
        parsed = urlparse.urlparse(item)
        self.visited.add("%s://%s%s/%s/%s"%(parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query))

    def extend(self,iterable):
        for item in iterable:
            self.push(item)
    def __len__(self):
        return len(self.store)

class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    allowed_domains = ['10.16.13.2']
    start_urls = ['http://10.16.13.2:8000/wikipedia_es_all_2019-06/']
    max_visited = 100
    queue = Queue(max_visited)
    
    def parse(self, response):
        print(self.queue.current)
        print(len(self.queue.store))
        if self.queue.can_visit:
            self.queue.visit(response.url)
            soup = BeautifulSoup(response.css('body').get().replace('>','> '),'lxml')  
            a = [s.extract() for s in soup(['script','style','noscript'])]
            result = soup.get_text()
            item = WikipediaItem()
            item['title'] = response.css('title::text').get()
            item['url'] = response.url
            item['content'] = result
            yield item
            new_urls = [
                response.urljoin(url) for url in response.css('a::attr(href)').getall()
            ]
            self.queue.extend(new_urls)
            while len(self.queue) > 0 and self.queue.can_visit:
                url = self.queue.pop()
                if url not in self.queue.visited and url is not None:
                    yield scrapy.Request(url, callback=self.parse)
                    if not self.queue.can_visit:
                        break
                else:
                    break