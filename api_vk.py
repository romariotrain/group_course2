import requests
import datetime
import json
from pprint import pprint
from operator import itemgetter
from config import vktoken


class VkLoading():

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id


    def user_info(self):
        # Функция собирает информацию о пользователе по id
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.user_id,
                    'fields': 'first_name, last_name, deactivated, is_closed, city, sex, bdate',
                    'access_token': self.token,
                    'v': '5.1948'}
        res = requests.get(url, params=params)
        info_ = res.json()
        bdate = (((info_.get('response'))[0]).get('bdate'))
        is_closed = (((info_.get('response'))[0]).get('is_closed'))
        # Проверяет, показывается ли дата рождения в профиле пользователя
        # Если дата рождения закрыта или скрыт год рождения записывает 'None' в переменную 'age'
        if bdate == None:
            age = None
        elif len(bdate) < 8:
            age = None
        else:
            age = int((str(datetime.datetime.today()))[:4]) - int((bdate)[-4:])

        city = (((info_.get('response'))[0]).get('city', {'title': 'Мухосранск'})).get('title')
        sex = ((info_.get('response'))[0]).get('sex')
        first_name = (((info_.get('response'))[0]).get('first_name'))
        last_name = (((info_.get('response'))[0]).get('last_name'))
        info_user = {'vk_id': self.user_id, 'first_name': first_name, 'last_name': last_name, 'age': age, 'city': city, 'sex': sex, 'is_closed': is_closed}
        return info_user


    def users_search(self, city):
        # Функция ищет людей по необходимым параметрам,
        #  если ищет женщина, то подбираются мужчины ровесники и старше до 5 лет
        #  если ищет мужчина, то подбираются женщины ровесники и младше до 5 лет
        url = 'https://api.vk.com/method/users.search'
        user_info = self.user_info()
        sex = None
        age_from = None
        age_to = None

        if user_info.get('sex') == 1:
            sex = 2
            age_from = user_info.get('age')
            age_to = user_info.get('age') + 5
        elif user_info.get('sex') == 2:
            sex = 1
            age_from = user_info.get('age') - 5
            age_to = user_info.get('age')

        params = {'count': '1000',
                    'fields': 'city, bdate',
                    'age_from': age_from,
                    'age_to': age_to,
                    'sex': sex,
                    'hometown': user_info.get('city'),
                    'access_token': self.token,
                    'v': '5.1948'}
        users_search = requests.get(url, params=params)
        search_users = users_search.json()
        # Отсеиваем людей с заблокированными профилями
        # и тех, кто на данный момент не проживает в городе пользователя
        # Вносим id людей в список
        user_list = []
        for user in search_users['response']['items']:
            if user.get('is_closed') == False and \
                    (user.get('city', {'title': 'Мухосранск'})).get('title') == city:
                user_list.append(str(user.get('id')))
        user = user_list.pop()
        # Возвращаем и удаляем последний элемент списка
        # Полученный список записываем в файл
        with open('user_list.txt', "w") as file:
            file.write(','.join(user_list))
        return user




    def users_search_next(self):
        # Читаем список поиска из файла
        with open('user_list.txt', "r") as file:
            user_str = file.read()
            user_list = user_str.split(',')
        user = user_list.pop()
        # Возвращаем и удаляем последний элемент списка
        # Полученный список записываем в файл
        with open('user_list.txt', "w") as file:
            file.write(','.join(user_list))
        return user


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
        # Функция отбирает лучшие фото по количеству лайков и создает список из трех (либо менее) фотографий
        inf_photo = self.user_photos()
        photo_dict = {}
        photo_id = None
        for select_photo in inf_photo['response']['items']:
            photo_dict[select_photo['id']] = select_photo['likes']['count']
        sorted_photo = sorted(photo_dict.items(), key=itemgetter(1))
        sorted_photo.reverse()
        best_photos = []
        key = 1
        for photo in sorted_photo:
            best_photos.append(f'photo{self.user_id}_{photo[0]}')
            key +=1
            if key > 3:
                break
        return best_photos


def user_info(user_id):
    vk = VkLoading(token=vktoken, user_id=user_id)
    return vk.user_info()


def users_search(user_id, city):
    vk = VkLoading(token=vktoken, user_id=user_id)
    return vk.users_search(city)


def users_search_next(user_id):
    vk = VkLoading(token=vktoken, user_id=user_id)
    return vk.users_search_next()


def links_photos(user_id):
    vk = VkLoading(token=vktoken, user_id=user_id)
    return vk.links_photos()

