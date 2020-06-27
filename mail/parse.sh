#!/bin/bash

unset http_proxy
unset https_proxy
cd /var/www/scrapy_parser/mail/mail/spiders/
scrapy crawl mail_spider -L WARNING
cd /var/www/scrapy_parser/mail/info/info/spiders/
scrapy crawl info_v1 -L WARNING
