from tokens import token_bot
from database import *
from functions import *
from random import randrange


import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


vk = vk_api.VkApi(token=token_bot)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })


def write_photo(user_id, attachment):
    vk.method('messages.send', {'user_id': user_id, 'attachment': attachment,  'random_id': 0, })


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.lower()

            if request == "привет":
                write_msg(event.user_id,
                          f"Привет, {get_name()}. Для поиска пары напишите start, для завершения работы бота - пока")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
                break
            elif request == "start":
                hometown = get_hometown()
                birthday = get_birthday()[0]
                pol = get_pol()[0]
                if hometown == '' or birthday == '' or pol == '':
                    write_msg(event.user_id,
                              "Для поиска не хватает данных. Проверьте и заполните профиль в ВК (город, дата рождения, пол). Попытайте счастья снова, написав мне start")
                    break
                create_table()
                offset = 0
                f_user = find_user(offset)
                while find_client(event.user_id, f_user['items'][0]['id']) == [(1,)] or \
                        find_user(offset)['items'][0]['is_closed'] != False:
                    offset += 1
                    f_user = find_user(offset)
                    continue
                write_msg(event.user_id,
                          f"Лови, {get_name()}, https://vk.com/{find_user(offset)['items'][0]['domain']}")
                add_client(event.user_id, find_user(offset)['items'][0]['id'])
                write_photo(event.user_id, f"photo{find_user(offset)['items'][0]['id']}_{get_photos_id(find_user(offset)['items'][0]['id'])[0][1]}")
                write_photo(event.user_id, f"photo{find_user(offset)['items'][0]['id']}_{get_photos_id(find_user(offset)['items'][0]['id'])[1][1]}")
                write_photo(event.user_id, f"photo{find_user(offset)['items'][0]['id']}_{get_photos_id(find_user(offset)['items'][0]['id'])[2][1]}")
                write_msg(event.user_id, f"Для нового поиска напишите start, для завершения работы бота - пока")
            else:
                write_msg(event.user_id,
                          "Не понял... Для поиска пары напишите start, для завершения работы бота - пока")
