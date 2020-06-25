# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class N1Pipeline:
    def process_item(self, item, spider):
        return item

    def __init__(self):
        self.conn = sqlite3.connect('/Users/nikitatonkoskurov/PycharmProjects/domofound2/db.sqlite3')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        house_id_val = item['house_id']
        img_val = item['img']
        title_val = item['title']
        link_val = item['link']
        price_val = item['price']
        address_val = item['address']
        time_created_val = item['time_created']
        data_val = item['data']
        host_val = item['host']
        self.cursor.execute('SELECT house_id FROM base_housemodel WHERE house_id=?', (house_id_val,))
        a = self.cursor.fetchone()
        if a:
            print('This row is already exist')
        else:
            self.cursor.execute(
                f"INSERT INTO base_housemodel VALUES (NULL ,?,?,?,?,?,?,?,?,NULL,?)",
                (house_id_val, title_val, link_val, price_val, address_val, data_val, time_created_val, host_val,
                 img_val))
            self.conn.commit()
