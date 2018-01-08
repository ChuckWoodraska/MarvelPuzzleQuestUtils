# -*- coding: utf-8 -*-

# Scrapy settings for quotesbot project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'mpq_utils'

SPIDER_MODULES = ['mpq_utils.spiders']
NEWSPIDER_MODULE = 'mpq_utils.spiders'

# ITEM_PIPELINES = {'mpq_utils.pipelines.BaseCharacterPipeline': 100, 'mpq_utils.pipelines.RosterCharacterPipeline': 200}
