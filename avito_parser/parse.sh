#!/bin/bash
export http_proxy="http://mrniki002:B0m6TxL@93.190.44.231:65233"
export https_proxy="https://mrniki002:B0m6TxL@93.190.44.231:65233"
cd /var/www/scrapy_parser/avito_parser/avito/avito/spiders/
scrapy crawl avito -L WARNING
cd /var/www/scrapy_parser/avito_parser/info/info/spiders/
scrapy crawl info_v1 -L WARNING
