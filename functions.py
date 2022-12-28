from tokens import token_user
import vk_api
from datetime import datetime

vku = vk_api.VkApi(token=token_user)


def get_name():
    user = vku.method("account.getProfileInfo")
    name = user['first_name']
    return name


def get_hometown():
    user = vku.method("account.getProfileInfo")
    hometown = user['home_town']
    return hometown


def get_birthday():
    user = vku.method("account.getProfileInfo")
    birthday = user['bdate']
    date_list = birthday.split('.')
    year1 = int(date_list[2]) - 5
    year2 = int(date_list[2]) + 5
    return birthday, year1, year2


def get_pol():
    user = vku.method("account.getProfileInfo")
    pol = user['sex']
    if pol == 2:
        find_pol = 1
    if pol == 1:
        find_pol = 2
    return pol, find_pol


def find_user(offset):
    user_find = vku.method("users.search", {'sex': get_pol()[1],
                                            'age_from': datetime.now().year-get_birthday()[2],
                                            'age_to': datetime.now().year-get_birthday()[1],
                                            'hometown': get_hometown(),
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