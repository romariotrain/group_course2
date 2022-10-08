import psycopg2
import api_vk
import config
import db_postgresql
import vk_bot


if __name__ == '__main__':  
    TOKEN_VK = config.vktoken # Токен от бота VK
    PASSWORD_SQL = config.password_sql

    # Создается подключение к БД через обьект conn. 
    # database - имя БД, user - имя при регистрации в postgress, password - пароль от user 
    with psycopg2.connect(database = "tinder_min", user = "postgres", password = PASSWORD_SQL) as conn:        
        # Через обьект cur создаются запросы к БД 
        with conn.cursor() as cur:            
            db = db_postgresql.DataBase(conn, cur) 
            table = db_postgresql.Client(conn, cur)

            # Создать необходимые таблицы в БД
            name_table = 'person'
            print(db.create_table(name_table))
            name_table = 'best_photo'
            print(db.create_table(name_table)) 
            name_table = 'selected'
            print(db.create_table(name_table)) 


            # Добавить данные юзера в БД
            user_info = {
                'vk_id': 1607,
                'first_name': 'Ira',
                'last_name': 'Smirnova',
                'sex': 'girl',
                'age': 20,
                'city': 'Москва'
            }
            print(table.add_person(user_info))        

            # Добавить страницу в список избранных (создать пару)
            elector_id = 1607
            favorite_info = {
                'vk_id': 829,
                'first_name': 'Gena',
                'last_name': 'Smirnoff',
                'sex': 'men',
                'age': 25,
                'city': 'Tomsk'
                }
            photo_list = ['photo-86093450_456239309', 
                'photo-86093450_456239390', 
                'photo-86093450_456239111'
                ]
            print(table.add_favorite(elector_id, favorite_info, photo_list))  

            # Вывести список избранных
            vk_id = 1
            print(table.outputs_list(vk_id))  

    conn.close()