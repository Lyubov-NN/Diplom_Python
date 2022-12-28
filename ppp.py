from tokens import token_user
import requests

def get_photos_id(user_id):
    """ПОЛУЧЕНИЕ ID ФОТОГРАФИЙ С РАНЖИРОВАНИЕМ В ОБРАТНОМ ПОРЯДКЕ"""
    url = 'https://api.vk.com/method/photos.getAll'
    params = {'access_token': token_user,
              'type': 'album',
              'owner_id': user_id,
              'extended': 1,
              'count': 25,
              'v': '5.131'}
    resp = requests.get(url, params=params)
    dict_photos = dict()
    resp_json = resp.json()
    try:
        dict_1 = resp_json['response']
        list_1 = dict_1['items']
        for i in list_1:
            photo_id = str(i.get('id'))
            i_likes = i.get('likes')
            if i_likes.get('count'):
                likes = i_likes.get('count')
                dict_photos[likes] = photo_id
        list_of_ids = sorted(dict_photos.items(), reverse=True)
        print(resp_json)
        print(list_of_ids)
    except KeyError:
        self.write_msg(user_id, 'Ошибка получения токена')

get_photos_id(339235457)