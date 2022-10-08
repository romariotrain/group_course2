# import os
import requests
import datetime
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
                  'fields': 'first_name, last_name, deactivated, is_closed, city, sex, bdate',
                  'access_token': self.token,
                  'v': '5.1948'}
        res = requests.get(url, params=params)
        info_ = res.json()
        bdate = (((info_.get('response'))[0]).get('bdate'))
        is_closed = (((info_.get('response'))[0]).get('is_closed'))

        if bdate == None:
            age = None
        elif len(bdate) < 8:
            age = None
        else:
            age = int((str(datetime.datetime.today()))[:4]) - int((bdate)[-4:])

        city = (((info_.get('response'))[0]).get('city')).get('title')
        sex = ((info_.get('response'))[0]).get('sex')
        first_name = (((info_.get('response'))[0]).get('first_name'))
        last_name = (((info_.get('response'))[0]).get('last_name'))

        user_info = {'first_name': first_name, 'last_name': last_name, 'age': age, 'city': city, 'sex': sex, 'is_closed': is_closed}

        return user_info


    def users_search(self):
        url = 'https://api.vk.com/method/users.search'
        user_info = self.user_info()
        if user_info.get('sex') == 1:
            sex = 2
        elif user_info.get('sex') == 2:
            sex = 1
        else:
            print('Укажите пол')
        params = {'count': '1000',
                  'fields': 'city',
                  'age_from': user_info.get('age'),
                  'age_to': user_info.get('age'),
                  'sex': sex,
                  'hometown': user_info.get('city'),
                  'access_token': self.token,
                  'v': '5.1948'}
        users_search = requests.get(url, params=params)
        return users_search.json()

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







def user_info(user_id):
    vk = VkLoading(token=vktoken, user_id=user_id)
    pprint(vk.user_info())

def users_search(user_id):
    vk = VkLoading(token=vktoken, user_id=user_id)
    pprint(vk.users_search())
