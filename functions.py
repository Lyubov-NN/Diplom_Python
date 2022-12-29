from tokens import *
from datetime import datetime
from random import randrange
import vk_api

vk = vk_api.VkApi(token=token_bot)
vku = vk_api.VkApi(token=token_user)

from vk_api.longpoll import VkLongPoll, VkEventType

longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })


def write_photo(user_id, attachment):
    vk.method('messages.send', {'user_id': user_id, 'attachment': attachment, 'random_id': 0, })


def get_name(user_id):
    try:
        user = vku.method("account.getProfileInfo")
        name = user['first_name']
        return name
    except vk_api.exceptions.VkApiError:
        write_msg(user_id, 'Ошибка токена, введите токен в переменную - token_user')


def get_hometown(user_id):
    try:
        user = vku.method("account.getProfileInfo")
        hometown = user['home_town']
        if hometown == '':
            write_msg(user_id, "Для поиска не хватает данных. Введите город поиска")
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        hometown = event.text
                        return hometown
        print(hometown)
        return hometown
    except vk_api.exceptions.VkApiError:
        write_msg(user_id, 'Ошибка токена, введите токен в переменную - token_user')
# get_hometown(6186222)

def get_birthday(user_id):
    try:
        user = vku.method("account.getProfileInfo")
        birthday = user['bdate']
        date_list = birthday.split('.')
        year1 = int(date_list[2]) - 5
        year2 = int(date_list[2]) + 5
        if birthday == '':
            write_msg(user_id, "Для поиска не хватает данных. Введите год рождения")
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        year1 = int(event.text) - 5
                        year2 = int(event.text) + 5
        return birthday, year1, year2
    except vk_api.exceptions.VkApiError:
        write_msg(user_id, 'Ошибка токена, введите токен в переменную - token_user')


def get_pol(user_id):
    try:
        user = vku.method("account.getProfileInfo")
        pol = user['sex']
        if pol == 2:
            find_pol = 1
        if pol == 1:
            find_pol = 2
        if pol == 0:
            write_msg(user_id, "Для поиска не хватает данных. Введите пол поиска (1 - женщина, 2 - мужчина)")
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        find_pol = event.text
        return pol, find_pol
    except vk_api.exceptions.VkApiError:
        write_msg(user_id, 'Ошибка токена, введите токен в переменную - token_user')


def find_user(user_id, pol, age_from, age_to, hometown, offset):
    user_find = vku.method("users.search", {'sex': pol,
                                            'age_from': age_from,
                                            'age_to': age_to,
                                            'hometown': hometown,
                                            'offset': offset,
                                            'has_photo': 1,
                                            'fields': 'is_closed, id, domain, first_name, last_name',
                                            'status': '1' or '6',
                                            'count': 1})
    return user_find


def get_photos_id(owner_id):
    photos = vku.method("photos.getAll", {'owner_id': owner_id, 'type': 'album', 'extended': 1})
    dict_photos = dict()
    list_1 = photos['items']
    for i in list_1:
        photo_id = str(i.get('id'))
        i_likes = i.get('likes')
        if i_likes.get('count'):
            likes = i_likes.get('count')
            dict_photos[likes] = photo_id
    list_of_ids = sorted(dict_photos.items(), reverse=True)
    return list_of_ids

# get_photos_id(339235457)
