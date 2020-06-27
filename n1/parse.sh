#!/bin/bash

cd /var/www/scrapy_parser/n1/n1/spiders/
scrapy crawl n1_spider -L WARNING
cd /var/www/scrapy_parser/n1/info/info/spiders/
scrapy crawl info_v1 -L WARNING
