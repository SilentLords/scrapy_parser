# -*- coding: utf-8 -*-
import csv
import sqlite3

import scrapy


class N1SpiderSpider(scrapy.Spider):
    name = 'n1_spider'
    allowed_domains = ['tumen.n1.ru']
    start_urls = ['https://tumen.n1.ru/kupit/kvartiry/?sort=-date&limit=50']
    link_pool = []

    def parse(self, response):
        cards = response.css('.living-list-card')

        for card in cards:
            if self.check_db(card.css('a.link::attr(href)').get().split('w/')[1].replace('/', '')):
                self.link_pool.append(response.urljoin(card.css('a.link::attr(href)').get()))
            yield ({
                'house_id': card.css('a.link::attr(href)').get().split('w/')[1].replace('/', ''),
                "link": response.urljoin(card.css('a.link::attr(href)').get()),
                "title": card.css('a.link > span::text').get(),
                "price": card.css('.living-list-card-price__item::text').get().replace(' ', ''),
                'address': card.css('a.link > span::text').get().split(',')[1] + ' ' +
                           card.css('a.link > span::text').get().split(',')[2] + ' ' + card.css(
                    '.living-list-card__inner-block::text').get() + ' ' + card.css(
                    'span.living-list-card-city-with-estate__item::text').get(),
                "img": card.css('.offer-list-preview__item > img::attr(src)').get(),
                'time_created': '',
                'data': '',
                'host': 'tumen.n1.ru'
            })
            # print(card.css('.offer-list-preview__item > img::attr(src)').get())
        self.save()

    def check_db(self, house_id_val):
        conn = sqlite3.connect('/var/www/dom/src/db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT house_id FROM base_housemodel WHERE house_id=?', (house_id_val,))
        a = cursor.fetchone()
        if a:
            return False
        else:
            return True

    def save(self):
        # print('save', self.link_pool)
        with open('../../info/info/spiders/links.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=";")
            for link in self.link_pool:
                writer.writerow([link])
