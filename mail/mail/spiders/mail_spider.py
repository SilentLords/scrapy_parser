# -*- coding: utf-8 -*-
import csv
import sqlite3

import scrapy


class MailSpider(scrapy.Spider):
    name = 'mail_spider'
    allowed_domains = ['tumn.realty.mail.ru']
    start_urls = ['https://tumn.realty.mail.ru/sale/living/?sort=date&sort_direct=desc']
    link_pool = []

    def parse(self, response):
        cards = response.css('.p-instance')
        for card in cards:
            if self.check_db(card.css('a.p-instance__title::attr(href)').get().split('-')[-1].replace('/', '')):
                self.link_pool.append(card.css('a.p-instance__title::attr(href)').get())
            yield ({

                'house_id': card.css('a.p-instance__title::attr(href)').get().split('-')[-1].replace('/', ''),
                "link": card.css('a.p-instance__title::attr(href)').get(),
                "title": card.css('a.p-instance__title::text').get(),
                "price": int("".join([x for x in card.css('span.p-instance__title::text').get() if ord(x) < 128])),
                'address': ''.join(card.css('a.p-instance__title::text').get().split(',')[1:]),
                "img": card.css('img.photo__pic::attr(src)').get(),
                'time_created': card.css('.p-instance__param.js-ago::attr(datetime)').get(),
                'data': '',
                'host': self.allowed_domains[0]})
            print(card.css('a.p-instance__title::attr(href)').get().split('-')[-1].replace('/', ''))
            print(card.css('a.p-instance__title::text').get())
            print(card.css('a.p-instance__title::attr(href)').get())
            print(int("".join([x for x in card.css('span.p-instance__title::text').get() if ord(x) < 128])))
            print(''.join(card.css('a.p-instance__title::text').get().split(',')[1:]))
            print(card.css('img.photo__pic::attr(src)').get())
            print(card.css('.p-instance__param.js-ago::attr(datetime)').get())
            print('-----------------------------------------------\n')
        self.save()

    # for card in cards:
    #     if self.check_db(card.css('a.link::attr(href)').get().split('w/')[1].replace('/', '')):
    #         self.link_pool.append(response.urljoin(card.css('a.link::attr(href)').get()))
    #     yield ({
    #         'house_id': card.css('a.link::attr(href)').get().split('w/')[1].replace('/', ''),
    #         "link": response.urljoin(card.css('a.link::attr(href)').get()),
    #         "title": card.css('a.link > span::text').get(),
    #         "price": card.css('.living-list-card-price__item::text').get(),
    #         'address': card.css('a.link > span::text').get().split(',')[1] + ' ' +
    #                    card.css('a.link > span::text').get().split(',')[2] + ' ' + card.css(
    #             '.living-list-card__inner-block::text').get() + ' ' + card.css(
    #             'span.living-list-card-city-with-estate__item::text').get(),
    #         "img": card.css('.offer-list-preview__item > img::attr(src)').get(),
    #         'time_created': '',
    #         'data': '',
    #         'host': 'tumen.n1.ru'
    #     })
    # print(card.css('.offer-list-preview__item > img::attr(src)').get())

    def check_db(self, house_id_val):
        conn = sqlite3.connect('/Users/nikitatonkoskurov/PycharmProjects/domofound2/db.sqlite3')
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
