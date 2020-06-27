# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
import sqlite3


class InfoPipeline:
    def __init__(self):
        self.conn = sqlite3.connect('/var/www/dom/src/db.sqlite3')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_images(self, house_id_val, images):
        self.cursor.execute('SELECT id FROM base_housemodel WHERE house_id=?', (house_id_val,))
        house_id = self.cursor.fetchone()
        if house_id:
            for image in images:
                # print(image)
                self.cursor.execute(
                    f"INSERT INTO base_image VALUES (NULL ,?,?)", (house_id[0], image))
            self.conn.commit()
        else:
            print('Cant find house with this house_id')

    def store_db(self, item):
        # print(item['floor_count'])
        house_id_val = int(item['house_id'].replace(' ', '').split('?')[0])
        type_of_participation_val = item['type_of_participation']
        official_builder_val = item['official_builder']
        name_of_build_val = item['name_of_build']
        decoration_val = item['decoration']
        floor_val = item['floor']
        floor_count_val = item['floor_count']
        house_type_val = item['house_type']
        num_of_rooms_val = item['num_of_rooms'].replace(' ', '')
        total_area_val = item['total_area'].replace('м²','').strip().replace(',', '.')
        living_area_val = item['living_area'].replace('м²','').strip().replace(',', '.')
        kitchen_area_val = item['kitchen_area'].replace('м²','').strip().replace(',', '.')
        deadline_val = item['deadline']
        phone_val = re.sub(r'\+|\(|\)|\-| ','',item['phone'])
        self.cursor.execute('SELECT phone FROM base_houseinfo WHERE house_id=?', (house_id_val,))

        if num_of_rooms_val == 'студии' or num_of_rooms_val == "своб. планировка":
            print('Студия или своб. планировка')
        else:
            if int(num_of_rooms_val) >= 5:
                num_of_rooms_val = '5+к'
            else:
                num_of_rooms_val = f'{int(num_of_rooms_val)}к'
        if total_area_val == '':
            total_area_val = 0
        else:
            total_area_val = float("".join([x for x in total_area_val if ord(x) < 128]))
        if living_area_val == '':
            living_area_val = 0
        else:
            living_area_val = float("".join([x for x in living_area_val if ord(x) < 128]))
        if kitchen_area_val == '':
            kitchen_area_val = 0
        else:
            kitchen_area_val = float("".join([x for x in kitchen_area_val if ord(x) < 128]))
        self.cursor.execute('SELECT phone FROM base_houseinfo WHERE house_id=?', (house_id_val,))
        if self.cursor.fetchone():
            print('this row is already exist')
        else:
            self.cursor.execute(
                f"INSERT INTO base_houseinfo VALUES (NULL ,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (house_id_val, type_of_participation_val, official_builder_val, name_of_build_val, decoration_val,
                 floor_val,
                 floor_count_val, house_type_val, num_of_rooms_val, living_area_val, kitchen_area_val, deadline_val,
                 phone_val, total_area_val))
            self.conn.commit()
            self.store_images(house_id_val, item['images'])
            self.cursor.execute("SELECT id FROM base_houseinfo where house_id=?", (house_id_val,))

            house_info_id_val = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT house_id FROM base_housemodel where house_id=?", (house_id_val,))
            l = self.cursor.fetchone()
            print(f'l = {l}')
            if l:
                print('Find House')
                h_id = l[0]
            else:
                h_id = None
            print(h_id)
            if h_id:
                print('Add info to house')
                self.cursor.execute(
                    f"UPDATE base_housemodel SET house_info_id = {house_info_id_val} where house_id = {h_id}")
                self.conn.commit()
                self.cursor.execute(
                    f"UPDATE base_housemodel SET data=? where house_id = {h_id}", (item['data'],))
                self.conn.commit()

        # self.conn.close()
