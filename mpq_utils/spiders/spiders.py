import scrapy
from scrapy.http.request import Request

from mpq_utils.items import *
from scrapy.utils.log import configure_logging
import logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)


def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

class MPQBaseCharacterSpider(scrapy.Spider):
    name = "base_character"
    start_urls = [
        'http://marvelpuzzlequest.wikia.com/wiki/Category:Characters',
    ]
    base = 'http://marvelpuzzlequest.wikia.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'mpq_utils.pipelines.BaseCharacterPipeline': 100
        }
    }

    def parse(self, response):
        for table in response.xpath('//table'):
            for tr in table.xpath('./tr')[1:]:
                item = MPQCharacter()
                character_url = tr.xpath('./td/a/@href').extract_first()
                # THESE WILL ERROR BECAUSE OF MISSING STATS
                # Thor:Gladiator, Spider-Man:Back in Black, Devil Dinosaur:Gigantic Reptile, Howard The Duck:A Duck
                # Angel:All New X-Men
                if character_url is not None:
                    request = Request(MPQBaseCharacterSpider.base + character_url, callback=self.parse_character)
                    item['name'] = tr.xpath('./td/a/text()').extract_first()
                    item['secondary_name'] = tr.xpath('./td/text()').extract_first()
                    request.meta['item'] = item
                    yield request

    def parse_character(self, response):
        item = response.meta['item']
        # Valid page?
        if response.xpath('//aside/div').extract():
            powers = response.xpath('//aside/div')[2].xpath('./div/text()')[0].extract().split(', ')
            if len(powers) == 3:
                item['power1_color'] = powers[0]
                item['power2_color'] = powers[1]
                item['power3_color'] = powers[2]
            else:
                item['power1_color'] = powers[0]
                item['power2_color'] = powers[1]
                item['power3_color'] = 'Hidden'

            stats_pages = response.xpath("//div[contains(@id, 'flytabs_')]//a/@href")
            if stats_pages:
                for index, stats_page in enumerate(stats_pages):
                    request = Request(MPQBaseCharacterSpider.base + stats_page.extract(), callback=self.parse_stats)
                    request.meta['item'] = item
                    # if index == len(stats_pages)-1:
                    #     request.meta['last_page'] = True
                    # else:
                    #     request.meta['last_page'] = False
                    yield request
            else:
                if 'character_stats' not in item:
                    item['character_stats'] = []
                table = response.xpath('//table')[0]
                for tr in table.xpath('./tr')[1:]:
                    stats = tr.xpath('./td/text()').extract_first()
                    if is_number(stats):
                        new_stat = []
                        for td in tr.xpath('./td/text()'):
                            new_stat.append(td.extract())
                        item['character_stats'].append(new_stat)
                yield item

    def parse_stats(self, response):
        item = response.meta['item']
        if 'character_stats' not in item:
            item['character_stats'] = []
        table = response.xpath('//table')
        for tr in table.xpath('//tr')[1:]:
            item['character_stats'].append(tr.xpath('./td/text()').extract())
        # if response.meta['last_page']:
        #     yield item
        # Not sure of the best way to handle this. The problem is each stats page is an async call so we would have to
        # block to know exactly what page we are on to know if all the stats were collected.
        if len(item['character_stats']) in [130, 227, 296, 301]:
            yield item


class MPQRosterCharacterSpider(scrapy.Spider):
    name = "roster_character"
    start_urls = [
        'https://mpq.gamependium.com/rosters/cwoodraska/spreadsheet/',
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'mpq_utils.pipelines.RosterCharacterPipeline': 200
        }
    }

    def parse(self, response):
        table = response.xpath('//table')
        for tr in table.xpath('//tr[contains(@class, "recruited")]'):
            item = MPQRosterCharacter()
            item['name'] = tr.xpath('./td/a/text()').extract_first()
            item['secondary_name'] = tr.xpath('./td/text()')[0].extract()
            # print(tr.xpath('./td/text()')[2].extract())
            item['stars'] = tr.xpath('./td/text()')[1].extract()
            item['level'] = tr.xpath('./td/text()')[4].extract()
            covers = tr.xpath('./td/text()')[2].extract().split('/')
            if len(covers) == 3:
                item['power1_level'] = covers[0]
                item['power2_level'] = covers[1]
                item['power3_level'] = covers[2]
            else:
                item['power1_level'] = covers[0]
                item['power2_level'] = covers[1]
                item['power3_level'] = 0
            yield item


if __name__ == '__main__':
    pass