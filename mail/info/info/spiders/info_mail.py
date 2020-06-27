# -*- coding: utf-8 -*-
import scrapy
from inline_requests import inline_requests


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
    allowed_domains = ['realty.mail.ru']

    @inline_requests
    def parse(self, response):
        print(f'processing: {response.url}')
        Headers = {
            ':authority': 'tumn.realty.mail.ru',
            'cookie': 'mrcu=A8955EA69253407588504E942B05; b=zEcBAAAtNVcAAQAC; OTVET-8088=3; x_user_id=1667777051169219; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; VID=2V8KCI0W1fnx00000Q0qD4Hx::335783053:0-0-3c76e58-3bbed27:CAASEEIYHaAds7qa9qeE4dlKoP0acHbNqsAP-6HLu39TLJYMKY0QsaCF54puPXyQC234dZfUKZUrbaR0qNGv9dm3n6AVCIQ_YSkfAoLnrci7bhKB8BV0bUmZYGIaRmeKJtECve0ZpuOprHD-kN1rGGjW9FF2XYwbpRlyIHQsL5pJnZUYRBw; act=01e5e698ddb14a8fa226f66fb2a428dc; i=AQBSs/BeCQATAAgTBp0AAWIBARoCAYwDAWcKAW0KAbsBCAQBAQABkwIIZyJuAAHFAAFwAQEBAgECAgEIAgEJAgENAgESAgEXAgFsAgFgBQFhBQFoBQF0BQF2BQGgBQGhBQGkBQGmBQGpBQEQBgF6BgHFCwHICwHJCwHMCwHNCwFwDQF0DQF4DQGGDQHXDQG5YwHcBAgEAQEAAeEECQEB4gQKBBACzwc6BQgWByoCAQgEAQkEAWsEAZoEAQsIAUYKAdYGCAQBAQABvQcIBAGZFQE=; p=ED0CANfX6QAA; Mpop=1592833093:535d7b4e4972497e1905000017031f051c054f6c5150445e05190401041d55565d5657564c56551e505358525b5847434b5044594a135f5950551f4b40:domafound.admenistrator@mail.ru:; t=obLD1AAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAACAAAcDrgcA; o=domafound.admenistrator@mail.ru:233:AA==.s; s=ww=1639|wh=981|dpr=2|rt=1|octavius=1; realty_geo=2021596',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.142',
            'accept': '*/*',
            'referer': response.url}
        type_of_participation, official_builder, name_of_build, decoration, floor, floor_count, house_type, num_of_rooms, total_area, living_area, kitchen_area, deadline = ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        images = []
        # print(response.url)
        images_req = response.css('.grid__item::attr("data-original")').getall()
        for image in images_req:
            images.append(image)
        print('------------------------\n')
        # print(response.css('.p-gallery-wrap > .js-module::attr(onclick)').get().split('phone_full":')[1].replace('}}}}}}', '').replace('"',''))
        if response.css('.p-gallery-wrap > .js-module::attr(onclick)').get():
            num = response.css('.p-gallery-wrap > .js-module::attr(onclick)').get().split('phone_full":')[1].replace(
                '}}}}}}', '').replace('"', '')
        else:
            num = 00000000000
        par_list = []
        for item in response.css('.p-params__item'):
            # if item.css('span.color_gray::text').getall() == 'кухня':
            #     print('hui')
            #     par_list.append(
            #         [item.css('span.p-params__name::text').get(), item.css('span.p-params__value > span::text').getall()])
            par_list.append(
                [item.css('span.p-params__name::text').get(), item.css('span.p-params__value > span::text').get()])
        # print(par_list)

        for item in par_list:
            if item[0] == 'Комнат':
                num_of_rooms = item[1]
            if item[0] == 'Этаж / Всего':
                floor = item[1].split('/')[0].replace(' ', '')
                floor_count = item[1].split('/')[1].replace(' ', '')
            if item[0] == 'Площадь, м²':
                total_area = item[1]
            if item[0] == 'Тип дома':
                house_type = item[1]
        data = response.css(".toggle__item > div::text").get()

        # num = response.css('a.offer-card-contacts-phones__phone::attr(href)').get().replace('tel:+', '')
        # params = response.css('li.card-living-content-params-list__item')
        # par_list = []
        # for par in params:
        #     # print(par.css("span::text").getall())
        #     par_list.append(par.css("span::text").getall())
        # if par_list.__len__() > self.max_params_len:
        #     self.max_params_len = par_list.__len__()
        #     self.max_params = par_list
        # # print(par_list)
        # for item in par_list:
        #     if item[0] == "Общая площадь":
        #         total_area = item[1].replace('\xa0м', '')
        #     if item[0] == 'Этаж':
        #         floor = int(item[1].split(' из ')[0])
        #         floor_count = int(item[1].split(' из ')[1])
        #     if item[0] == 'Материал дома':
        #         house_type = item[1]
        #     if item[0] == 'Кухня':
        #         kitchen_area = item[1]
        # num_of_rooms = response.css('.deal-title::text').get().split(' ')[1]
        yield {
            'house_id': response.url.split('-')[-1].replace('/', '').replace('?osale2', '').replace('?osale1', ''),
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
            'images': images,
            'data': data}

        self.id_house += 1
        # print(f'Parsed links: {self.id_house} of{self.links.__len__()} ')
        # # print(self.links)
        # # sleep(8)
        if self.links.__len__() > self.id_house:
            yield scrapy.Request(self.links[self.id_house],
                                 callback=self.parse, dont_filter=True)
        else:
            # print(self.max_params_len, self.max_params)
            print('save')

    def save(self):
        with open('info.json', "w", encoding="utf8") as f:
            f.write(json.dumps(self.all_json_data, ensure_ascii=False, indent=4))
