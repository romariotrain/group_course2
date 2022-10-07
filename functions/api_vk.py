# import os
import requests
import json
from pprint import pprint
from vktoken import vktoken
from operator import itemgetter


class VkLoading():
    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id


    def user_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.user_id,
                  'fields': 'city, sex, bdate',
                  'access_token': self.token,
                  'v': '5.1948'}
        res = requests.get(url, params=params)
        info_ = res.json()
        bdate = ['response']['bdate']
        # bdate = (((info_.get('response'))[0]).get('bdate'))
        city_id = (((info_.get('response'))[0]).get('city')).get('id')
        sex = ((info_.get('response'))[0]).get('sex')
        if sex == 2:
            sex = 1
        else:
            sex = 2

        info_search = [bdate, city_id, sex]

        return info_search


    def search_users(self):
        url = 'https://api.vk.com/method/users.search'
        user_info = self.user_info()
        params = {'count': '1',
                  'fields': 'bdate, domain, city',
                  'birth_year': user_info[0],
                  'sex': user_info[2],
                  'city': user_info[1],
                  'access_token': self.token,
                  'v': '5.1948'}
        search_ = requests.get(url, params=params)
        return search_.json()

    def user_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.user_id,
                  'extended': '1',
                  'album_id': 'profile',
                  'access_token': self.token,
                  'v': '5.1948'}
        res = requests.get(url, params=params)
        photos = res.json()
        return photos



    def links_photos(self):
        inf_photo = self.user_photos()
        photo_dict = {}
        # pprint(inf_photo)
        for select_photo in inf_photo['response']['items']:
            max_size = 0
            for size_photo in select_photo['sizes']:
                if size_photo['height'] >= max_size:
                    max_size = size_photo['height']
                    url_photo = size_photo['url']
                    size = size_photo['type']
            photo_dict[url_photo] = select_photo['likes']['count']
        sorted_photo = sorted(photo_dict.items(), key=itemgetter(1))
        best_photos = [sorted_photo[-1], sorted_photo[-2]]
        best_photos = dict(best_photos)
        return best_photos


    def tinder(self):
        search_users = self.search_users()
        output_list = []
        for select_users in search_users['response']['items']:
            out_list = []
            self.user_id = select_users['id']
            out_list.append(select_users['first_name'])
            out_list.append(select_users['last_name'])
            out_list.append(f'https://www.vk.com/{select_users["domain"]}')
            out_list.append(self.links_photos())
            output_list.append(out_list)

        return output_list







def search_vk(user_id):
    vk = VkLoading(token=vktoken, user_id=user_id)
    pprint(vk.tinder())
