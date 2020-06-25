# -*- coding: utf-8 -*-
import json
import re
from time import sleep
from inline_requests import inline_requests
import scrapy


def save_images(images):
    pass


class InfoSpider(scrapy.Spider):
    all_json_data = []
    links = []
    key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
    phone = ''
    id_house = 0
    max_params_len = 0
    max_params = []

    def start_requests(self):
        with open('links.csv') as f:
            self.links = f.read().splitlines()
            # print(self.links)
            yield scrapy.Request(url=self.links[0], callback=self.parse)

    name = 'info_v1'
    allowed_domains = ['tumen.n1.ru']

    @inline_requests
    def parse(self, response):
        print(f'processing: {response.url}')
        Headers = {
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.34; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 1.1.4322)',
            'accept': '*/*',
            'referer': response.url}
        type_of_participation, official_builder, name_of_build, decoration, floor, floor_count, house_type, num_of_rooms, total_area, living_area, kitchen_area, deadline = ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        images = []
        # print(response.url)
        images_req = response.css('.media-container > a::attr(href)').getall()
        for image in images_req:
            images.append(image)
        num = response.css('a.offer-card-contacts-phones__phone::attr(href)').get().replace('tel:+', '')
        params = response.css('li.card-living-content-params-list__item')
        par_list = []
        for par in params:
            # print(par.css("span::text").getall())
            par_list.append(par.css("span::text").getall())
        if par_list.__len__() > self.max_params_len:
            self.max_params_len = par_list.__len__()
            self.max_params = par_list
        # print(par_list)
        for item in par_list:
            if item[0] == "Общая площадь":
                total_area = item[1].replace('\xa0м', '')
            if item[0] == 'Этаж':
                floor = int(item[1].split(' из ')[0])
                floor_count = int(item[1].split(' из ')[1])
            if item[0] == 'Материал дома':
                house_type = item[1]
            if item[0] == 'Кухня':
                kitchen_area = item[1]
        num_of_rooms = response.css('.deal-title::text').get().split(' ')[1]
        yield {
            'house_id': response.url.split('w/')[1].replace('/', ''),
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
            'phone': num,
            'images': images}

        self.id_house += 1
        print(f'Parsed links: {self.id_house} of{self.links.__len__()} ')
        # print(self.links)
        # sleep(8)
        if self.links.__len__() > self.id_house:
            yield scrapy.Request(self.links[self.id_house],
                                 callback=self.parse, dont_filter=True)
        else:
            # print(self.max_params_len, self.max_params)
            print('save')

    def save(self):
        with open('info.json', "w", encoding="utf8") as f:
            f.write(json.dumps(self.all_json_data, ensure_ascii=False, indent=4))
