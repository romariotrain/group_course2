from random import randrange
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = 'vk1.a.lmZJ4sTwjbf8y5pxNVKN507gwWi7WcO43ju1S-gdsl7UDsEgMi-O8q-lpE0v1eMMJQ4PRaol1u7RDULnUmzWzLFElzJRM07tdU-Xvnzk8PIUm6HaHGp8paqqIYFRp6TSUsrAQ9YAf5uIzDbO1IVTz55-wk1RlCKOk_qvUrBlbMk5nEErI-8ztcQqBvEz1Zi9'

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


def send_photos(user_id, photo1, photo2, photo3):
    vk.method('messages.send', {'user_id': user_id, 'attachment': photo1, 'random_id': randrange(10 ** 7)})
    vk.method('messages.send', {'user_id': user_id, 'attachment': photo2, 'random_id': randrange(10 ** 7)})
    vk.method('messages.send', {'user_id': user_id, 'attachment': photo3, 'random_id': randrange(10 ** 7)})


def find_pair(user_id):
    # Здесь нужно сгенерировать три фотки в формате photo-216237919_457239023, которые будут отосланы, также
    # в какую-то переменную занести id человека, фото которого показываем.

    send_photos(user_id, photo1, photo2, photo3)
    keyboard = VkKeyboard()
    keyboard.add_button('Добавить в избранное')
    keyboard.add_button('Найти пару')
    keyboard.add_line()
    keyboard.add_button('Показать список избранных')
    keyboard.add_button('Закончить работу')
    write_msg(user_id, 'Выберите команду', keyboard1=keyboard)


# Это просто тестовые фото, не забыть удалить

photo1 = 'photo-178004949_456239022'
photo2 = 'photo-216237919_457239022'
photo3 = 'photo-216237919_457239021'


def bot_logic():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            user_id = event.user_id

            if event.to_me:
                text = event.text.lower()

                if text == "привет":
                    write_msg(user_id, f"Хай, напиши start, чтобы начать поиск фото")


                elif text == 'start':
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Найти пару')
                    write_msg(event.user_id, 'Lets go', keyboard)

                elif text == 'найти пару':
                    find_pair(user_id)

                elif text == 'добавить в избранное':
                    keyboard = VkKeyboard()
                    keyboard.add_button('найти пару')
                    keyboard.add_line()
                    keyboard.add_button('Показать список избранных')
                    keyboard.add_button('Закончить работу')

                    # Здесь надо добавлять id человека, фото которого показываем, в базу

                    write_msg(user_id, 'Выберите команду', keyboard1=keyboard)


                elif text == "закончить работу":
                    keyboard = VkKeyboard()
                    vk.method('messages.send', {'user_id': user_id, 'random_id': randrange(10 ** 7), 'message' : 'Пока((', 'keyboard':
                                                keyboard.get_empty_keyboard()})

                elif text == 'показать список избранных':
                    # Здесь выводим список избранных в определенном формате

                    keyboard = VkKeyboard()
                    keyboard.add_button('найти пару')
                    keyboard.add_button('Закончить работу')
                    write_msg(user_id, 'Выберите команду', keyboard1=keyboard)

                else:
                    write_msg(user_id, "Не поняла вашего ответа...")