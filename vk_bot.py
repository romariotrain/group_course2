from random import randrange
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from api_vk import user_info
from api_vk import users_search
from api_vk import users_search_next
from api_vk import links_photos
import config


TOKEN = config.vkbot
vk = vk_api.VkApi(token=TOKEN)
session_api = vk.get_api()
longpoll = VkLongPoll(vk)

def write_msg(user_id, message, keyboard1=None):
    post = {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)}
    if keyboard1 != None:
        post['keyboard'] = keyboard1.get_keyboard()
    else:
        post = post
    vk.method('messages.send', post)


def send_photos(user_id, photo_list, search_id):
    for photo in photo_list:
        vk.method('messages.send', {'user_id': user_id, 'attachment': photo, 'random_id': randrange(10 ** 7)})


def find_pair(user_id, user):
    info_user = user_info(user)
    photo_list = links_photos(user)
    send_photos(user_id, photo_list, user)
    keyboard = VkKeyboard()
    keyboard.add_button('Добавить в избранное')
    keyboard.add_button('Продолжить поиск')
    keyboard.add_line()
    keyboard.add_button('Показать список избранных')
    keyboard.add_button('Закончить работу')
    write_msg(user_id,  f"{info_user.get('first_name')} {info_user.get('last_name')},"
                        f" возраст - {info_user.get('age')},\n https://www.vk.com/id{user}")
    write_msg(user_id, 'Выберите команду', keyboard1=keyboard)


def bot_logic(table):
    user = None
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            user_id = event.user_id
            info_user = user_info(user_id)
            
            if event.to_me:
                text = event.text.lower()

                if text == "привет":
                    write_msg(user_id, f"Хай, напиши start, чтобы начать поиск фото")

                elif text == 'start':
                    if (user_info(user_id)).get('is_closed') == True:
                        write_msg(user_id, f"Откройте доступ к своему профилю и попробуйте снова")
                    elif (user_info(user_id)).get('age') == None:
                        write_msg(user_id, f"Установите в настройках профиля \"Показывать дату рождения\" и попробуйте снова")
                    elif (user_info(user_id)).get('sex') == 0:
                        write_msg(user_id, f"Установите в настройках профиля \"Пол\" и попробуйте снова")
                    elif (user_info(user_id)).get('city') == 'Мухосранск':
                        write_msg(user_id, f"Укажите в настройках профиля город проживания и попробуйте снова")
                    else:
                        print(info_user)
                        # print(table.add_person(info_user))
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button('Найти пару')
                        write_msg(event.user_id, 'Lets go', keyboard)

                elif text == 'найти пару':
                    user = users_search(user_id, (info_user.get('city')))
                    find_pair(user_id, user)

                elif text == 'продолжить поиск':
                    user = users_search_next(user_id)
                    find_pair(user_id, user)

                elif text == 'добавить в избранное':
                    keyboard = VkKeyboard()
                    keyboard.add_button('продолжить поиск')
                    keyboard.add_line()
                    keyboard.add_button('Показать список избранных')
                    keyboard.add_button('Закончить работу')

                    # Производим запись избранного в базу
                    info_user = user_info(user)
                    photo_list = links_photos(user)
                    print(info_user)
                    print(table.add_favorite(user_id, info_user, photo_list))
                    write_msg(user_id, 'Выберите команду', keyboard1=keyboard)

                elif text == "закончить работу":
                    keyboard = VkKeyboard()
                    vk.method('messages.send', {'user_id': user_id, 'random_id': randrange(10 ** 7), 'message' : 'Пока((', 'keyboard':
                                                keyboard.get_empty_keyboard()})

                elif text == 'показать список избранных':
                    # Здесь выводим список избранных в определенном формате
                    favorits = (table.outputs_list(int(user_id)))
                    index = 1
                    if favorits:
                        for favorit in favorits:
                            #Здесь в f строке нужно сделать вывод favorit
                            write_msg(user_id, f"{index}. {favorit[1]} {favorit[2]} https://www.vk.com/id{favorit[0]}")
                            index += 1
                    else:
                        write_msg(user_id, 'Список пуст')     

                    keyboard = VkKeyboard()
                    keyboard.add_button('Продолжить поиск')
                    keyboard.add_button('Закончить работу')
                    write_msg(user_id, 'Выберите команду', keyboard1=keyboard)

                else:
                    write_msg(user_id, "Не поняла вашего ответа...")




