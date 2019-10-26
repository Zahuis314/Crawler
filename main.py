import argparse
import scrapy,logging
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from wikipedia.spiders.wikipedia_spider import WikipediaSpider
from wikipedia.settings import EXPORT_SETTINGS
import algorithm

parser = argparse.ArgumentParser()
parser.add_argument('--mode', help='Scrap the websites', nargs='?', choices=['Calculate','Scrap','Both'], const='Calculate', default='Calculate')
parser.add_argument('--url', help='Url to consult')
parser.add_argument('--amount', help='Amount of website to show', type=int, nargs='?', const=10, default=10)
args = parser.parse_args()
print(args.amount)
print(args.mode)
if(args.mode in ['Scrap','Both']):
	process = CrawlerProcess(EXPORT_SETTINGS)
	process.crawl(WikipediaSpider)
	process.start()
	process.join()
if(args.mode in ['Calculate','Both']):
	algorithm.calculate(args.url,args.amount)