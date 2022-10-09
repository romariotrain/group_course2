from vk_bot import bot_logic
import db_postgresql
import config
import psycopg2

PASSWORD_SQL = config.password_sql


if __name__ == '__main__':
    # Создается подключение к БД через обьект conn.
    # database - имя БД, user - имя при регистрации в postgress, password - пароль от user
    with psycopg2.connect(database="tinder_min", user="postgres", password=PASSWORD_SQL) as conn:
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
        bot_logic()
    conn.close()