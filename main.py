import requests
import scrapy
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor

from py2neo import Graph, Node, Relationship, NodeMatcher
from scrapy.crawler import CrawlerRunner
from crochet import setup, wait_for
from scrapy.spiders import Rule
import configparser

from PageRankCalculations import PageRankCalculations

setup()
config = configparser.ConfigParser()
config.read('config.ini')


class crawl_pages(scrapy.Spider):
    def __init__(self):
        self.graph = Graph(uri=config['neo4j']['url'], auth=(config['neo4j']['username'], config['neo4j']['password']))

    name = "rank_crawler"
    start_urls = ["https://en.wikipedia.org/wiki/Cork_(city)"]
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse(self, response):
        # Create a node for the current page
        page_title = response.css('title::text').get()
        matcher = NodeMatcher(self.graph)
        page_node = matcher.match("Page", url=response.url).first()
        if page_node is None:
            page_node = Node("Page", url=response.url, name=page_title)
            self.graph.create(page_node)

        # Follow all links on the page recursively
        for next_page in response.css('a::attr(href)').getall():
            next_page_url = response.urljoin(next_page)
            next_page_response = requests.get(next_page_url)
            next_page_html = next_page_response.content.decode('utf-8')
            next_page_title = Selector(text=next_page_html).xpath('//title/text()').get()
            next_page_node = matcher.match("Page", url=next_page_url).first()
            if next_page_node is None:
                next_page_node = Node("Page", url=next_page_url, name=next_page_title)
                self.graph.create(next_page_node)

            # Create a relationship from the current page to the linked page
            relationship = Relationship(page_node, "LINKS", next_page_node, weight=1.0)
            self.graph.create(relationship)

            # Recursively crawl the linked page
            yield response.follow(next_page_url, self.parse)


@wait_for(50)
def run_spider():
    crawler = CrawlerRunner()
    d = crawler.crawl(crawl_pages)
    return d


if __name__ == "__main__":
    run_spider()
    pr = PageRankCalculations(config['neo4j']['url'],
                              config['neo4j']['username'],
                              config['neo4j']['password'])
    pr.calculate_page_rank()
    pr.close()
