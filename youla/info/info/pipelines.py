# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class InfoPipeline:
    def __init__(self):
        self.conn = sqlite3.connect('/Users/nikitatonkoskurov/PycharmProjects/domofound2/db.sqlite3')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_images(self, house_id_val, images):
        self.cursor.execute('SELECT id FROM base_housemodel WHERE house_id=?', (house_id_val,))
        house_id = self.cursor.fetchone()
        if house_id:
            for image in images:
                self.cursor.execute(
                    f"INSERT INTO base_image VALUES (NULL ,?,?)", (house_id[0], image))
            self.conn.commit()
        else:
            print('Cant find house with this house_id')

    def store_db(self, item):
        # print(item['floor_count'])
        house_id_val = int(item['house_id'].replace(' ', ''))
        type_of_participation_val = item['type_of_participation']
        official_builder_val = item['official_builder']
        name_of_build_val = item['name_of_build']
        decoration_val = item['decoration']
        floor_val = int(item['floor'].replace(' ', ''))
        floor_count_val = int(item['floor_count'].replace(' ', ''))
        house_type_val = item['house_type']
        num_of_rooms_val = item['num_of_rooms']
        total_area_val = item['total_area']
        living_area_val = item['living_area']
        kitchen_area_val = item['kitchen_area']
        deadline_val = item['deadline']
        phone_val = int(item['phone'].replace(' ', ''))
        self.cursor.execute('SELECT phone FROM base_houseinfo WHERE house_id=?', (house_id_val,))
        if self.cursor.fetchone():
            print('this row is already exist')
        else:
            self.cursor.execute(
                f"INSERT INTO base_houseinfo VALUES (NULL ,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (house_id_val, type_of_participation_val, official_builder_val, name_of_build_val, decoration_val,
                 floor_val,
                 floor_count_val, house_type_val, total_area_val, living_area_val, kitchen_area_val, deadline_val,
                 phone_val, num_of_rooms_val))
            self.conn.commit()
            self.store_images(house_id_val, item['images'])
            self.cursor.execute("SELECT id FROM base_houseinfo where house_id=?", (house_id_val,))

            house_info_id_val = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT house_id FROM base_housemodel where house_id=?", (house_id_val,))
            h_id = self.cursor.fetchone()[0]
            print(h_id)
            if h_id:
                print('Add info to house')
                self.cursor.execute(
                    f"UPDATE base_housemodel SET house_info_id = {house_info_id_val} where house_id = {h_id}")
                self.conn.commit()

        # self.conn.close()
