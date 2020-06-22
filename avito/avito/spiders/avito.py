# -*- coding: utf-8 -*-
import csv
import re
import sqlite3

import scrapy


def correct_price(text):
    return re.sub(r'\n|₽| ', '', text)


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    link_pool = []
    start_urls = ['https://www.avito.ru/tyumen/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1']
    page_count = 1
    cur_page = 1
    i = 0

    def parse(self, response):
        print("processing: " + response.url)
        products = response.css('.item__line')
        for item in products:
            data = ''
            if item.css('span.item-address-georeferences').get():
                geo = item.css(
                    'span.item-address-georeferences-item__content::text').get()
            else:
                geo = ''
            if self.check_db(item.css('a.snippet-link::attr(href)').get().split("._")[1]):
                self.link_pool.append(response.urljoin(item.css('a.snippet-link::attr(href)').get()))
            yield {
                'house_id': item.css('a.snippet-link::attr(href)').get().split("._")[1],
                'img': response.urljoin(item.css('img.large-picture-img::attr(src)').get()),
                'title': item.css('a.snippet-link::text').get(),
                'link': response.urljoin(item.css('a.snippet-link::attr(href)').get()),
                'price': int(correct_price(item.css('span.snippet-price::text').get())),
                'address': item.css('span.item-address__string::text').get() + ' ' + geo,
                'data': data,
                'time_created': item.css('div.snippet-date-info::text').get(),
                'host': self.allowed_domains[0]
            }
            # self.link_pool.append(response.urljoin(item.css('a.snippet-link::attr(href)').get()))
            self.i += 1
            # print(self.check_db(item.css('a.snippet-link::attr(href)').get().split("._")[1]))

        self.page_count -= 1
        self.cur_page += 1
        if self.page_count < 0:
            self.i = 0
            self.save()

        else:
            yield scrapy.Request(
                response.urljoin(self.start_urls[0] + '?p=' + str(self.cur_page)),
                callback=self.parse)

    def check_db(self, house_id_val):
        conn = sqlite3.connect('/Users/nikitatonkoskurov/PycharmProjects/domofound2/db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT house_id FROM base_housemodel WHERE house_id=?', (house_id_val,))
        a = cursor.fetchone()
        print(a)
        if a:
            return False
        else:
            return True

    def save(self):
        # print('save', self.link_pool)
        with open('../../../info/info/spiders/links.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=";")
            for link in self.link_pool:
                writer.writerow([link])
