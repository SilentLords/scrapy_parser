#!/bin/zsh

cd avito/avito/spiders/
scrapy crawl avito -L WARNING
cd ../../../info/info/spiders/
scrapy crawl info_v1 -L WARNING
