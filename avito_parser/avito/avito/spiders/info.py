# -*- coding: utf-8 -*-
import json
import re
from time import sleep
from inline_requests import inline_requests
import scrapy


class InfoSpider(scrapy.Spider):
    all_json_data = []
    links = []
    key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
    phone = ''
    id_house = 0

    def start_requests(self):
        with open('links.csv') as f:
            url = f.readline()
            self.links = f.read().splitlines()
            yield scrapy.Request(url=url, callback=self.parse)

    name = 'info'
    allowed_domains = ['avito.ru']

    @inline_requests
    def parse(self, response):
        # print(f'processing: {response.url}', 'Version 1')
        Headers = {
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.34; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 1.1.4322)',
            'accept': '*/*',
            'referer': response.url}
        type_of_participation, official_builder, name_of_build, decoration, floor, floor_count, house_type, num_of_rooms, total_area, living_area, kitchen_area, deadline = ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',

        # print(response.url)
        req = yield scrapy.Request(
            url=f'https://m.avito.ru/api/1/items/{response.url.split("._")[1]}/phone/?key={self.key}', headers=Headers)
        # print(req.body.decode("utf-8"))
        num = req.body.decode("utf-8").split('2B')[1].replace('"}}}', '')
        # print(num)

        for info_colum in response.css('li.item-params-list-item'):
            re_Info = info_colum
            re_Info = re.sub(r' |</li>', '', re_Info.extract().split(' </span>')[1])
            info_colum = info_colum.css('span.item-params-label::text').get()
            # print(info_colum, re_Info)
            if re.search(r'Тип участия', info_colum):
                type_of_participation = re_Info
            elif re.search(r'Официальный застройщик', info_colum):
                # print(re_Info)
                official_builder = re_Info
            elif re.search(r'Название новостройки', info_colum):
                name_of_build = re_Info
            elif re.search(r'Отделка', info_colum):
                decoration = re_Info
            elif re.search(r'Этаж', info_colum):
                floor = re_Info
            elif re.search(r'в доме', info_colum):
                # print(re_Info)
                floor_count = re_Info
            elif re.search(r'Тип дома', info_colum):
                house_type = re_Info
            elif re.search(r'Количество комнат', info_colum):
                num_of_rooms = re_Info
            elif re.search(r'Общая площадь', info_colum):
                total_area = re_Info
            elif re.search(r'Жилая площадь', info_colum):
                living_area = re_Info
            elif re.search(r'Площадь кухни', info_colum):
                kitchen_area = re_Info
            elif re.search(r'Срок сдачи', info_colum):
                deadline = re_Info
        yield {
            'id': self.id_house,
            'type_of_participation': type_of_participation,
            'official_builder': official_builder,
            'name_of_build': name_of_build,
            'decoration': decoration,
            "floor": floor,
            "floor_count": floor_count,
            "house_type": house_type,
            "num_of_rooms": num_of_rooms,
            "total_area": total_area,
            "living_area": living_area,
            "kitchen_area": kitchen_area,
            "deadline": deadline,
            'phone': num}

        self.id_house += 1
        print(f'Parsed links: {self.id_house} of{self.links.__len__()} ')
        # print(self.links)
        sleep(8)
        if self.links.__len__() > self.id_house:
            yield scrapy.Request(self.links[self.id_house],
                                 callback=self.parse, dont_filter=True)
        else:
            print('save')

    def save(self):
        with open('info.json', "w", encoding="utf8") as f:
            f.write(json.dumps(self.all_json_data, ensure_ascii=False, indent=4))
