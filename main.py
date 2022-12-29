from database import *
from functions import *


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.lower()

            if request == "привет":
                write_msg(event.user_id,
                          f"Привет, {get_name(event.user_id)}. Для поиска пары напишите start, для завершения работы бота - пока")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
                break
            elif request == "start":
                pol = get_pol(event.user_id)[1]
                age_from = datetime.now().year - get_birthday(event.user_id)[2]
                age_to = datetime.now().year - get_birthday(event.user_id)[1]
                hometown = get_hometown(event.user_id)
                create_table()
                offset = 0
                f_user = find_user(event.user_id, pol, age_from, age_to, hometown, offset)
                try:
                    while find_client(event.user_id, f_user['items'][0]['id']) == [(1,)] or \
                            find_user(event.user_id, pol, age_from, age_to, hometown, offset)['items'][0]['is_closed'] != False:
                        offset += 1
                        f_user = find_user(event.user_id, pol, age_from, age_to, hometown, offset)
                        continue
                except IndexError:
                    write_msg(event.user_id, 'Что-то пошло не так. Попробуем в следующий раз')
                write_msg(event.user_id,
                          f"Лови, {get_name(event.user_id)}, https://vk.com/{find_user(event.user_id, pol, age_from, age_to, hometown, offset)['items'][0]['domain']}")
                add_client(event.user_id, find_user(event.user_id, pol, age_from, age_to, hometown, offset)['items'][0]['id'])
                write_photo(event.user_id, f"photo{find_user(event.user_id, pol, age_from, age_to, hometown, offset)['items'][0]['id']}_{get_photos_id(find_user(event.user_id, pol, age_from, age_to, hometown, offset)['items'][0]['id'])[0][1]}")
                write_photo(event.user_id, f"photo{find_user(event.user_id, pol, age_from, age_to, hometown, offset)['items'][0]['id']}_{get_photos_id(find_user(event.user_id, pol, age_from, age_to, hometown, offset)['items'][0]['id'])[1][1]}")
                write_photo(event.user_id, f"photo{find_user(event.user_id, pol, age_from, age_to, hometown, offset)['items'][0]['id']}_{get_photos_id(find_user(event.user_id, pol, age_from, age_to, hometown, offset)['items'][0]['id'])[2][1]}")
                write_msg(event.user_id, f"Для нового поиска напишите start, для завершения работы бота - пока")
            else:
                write_msg(event.user_id,
                          "Не понял... Для поиска пары напишите start, для завершения работы бота - пока")
