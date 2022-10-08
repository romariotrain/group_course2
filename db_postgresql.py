class DataBase:
    """Класс для создания таблиц БД"""
    def __init__(self, conn, cur):
        self.conn = conn 
        self.cur = cur

    def create_table(self, name: str) -> str:
        if name == 'person':   
            # cur.execute - метод для написания запросов с помощью cur(курсор)                            
            self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS person(
                            person_id   SERIAL       PRIMARY KEY,
                            vk_id       INTEGER      UNIQUE NOT NULL,                
                            first_name  VARCHAR(30)  NOT NULL,   
                            last_name   VARCHAR(30)  NOT NULL,
                            sex         VARCHAR(8)   NOT NULL,
                            age         SMALLINT,
                            city        VARCHAR(50)
                            );
                            """)
            self.conn.commit()  # только после commit или fetch(one,many,all) происходит отправка запроса в БД
            return f'БД - создана таблица {name}'
        
        elif name == 'best_photo':                          
            self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS best_photo(
                            best_photo_id  SERIAL       PRIMARY KEY,
                            person_id      INTEGER      NOT NULL     REFERENCES person(vk_id),                
                            link_photo     VARCHAR(200) NOT NULL  
                            );                 
                            """)
            self.conn.commit()
            return f'БД - создана таблица {name}'
        
        elif name == 'selected':                          
            self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS selected(
                            selected_id  SERIAL   PRIMARY KEY,
                            elector_id   INTEGER  NOT NULL     REFERENCES person(vk_id),
                            favorite_id  INTEGER  NOT NULL     REFERENCES person(vk_id)       
                            );                 
                            """)
            self.conn.commit()
            return f'БД - создана таблица {name}'
        
        else:
            return 'Ошибка! Возможные имена "person", "best_photo", "selected"'


class Client:
    """Класс для работы с БД"""
    def __init__(self, conn, cur):
        self.conn = conn 
        self.cur = cur

    def checking_person(self, vk_id:int) -> bool:
        'Метод возвращет True если в таблице person есть такой id и Folse если нет'
        self.cur.execute("""
                        SELECT vk_id 
                        FROM   person
                        WHERE  vk_id = %s;
                        """ % (vk_id,))
        return bool(self.cur.fetchall())

    def checking_selected(self, elector_id:int,  favorite_id:int) -> bool:
        'Метод возвращет True если в таблице selected есть такой id и Folse если нет'
        self.cur.execute("""
                        SELECT elector_id, favorite_id 
                        FROM   selected
                        WHERE  elector_id = %s AND favorite_id = %s;
                        """ % (elector_id, favorite_id ))
        return bool(self.cur.fetchall())

    def add_person(self, user_info: dict)-> str:
        'Добавляет запись в таблицу person'
        flag = self.checking_person(user_info['vk_id'])        
        if not flag:      
            self.cur.execute("""
                            INSERT INTO person (vk_id, first_name, last_name, sex, age, city) 
                            VALUES ('%s', '%s', '%s', '%s', '%s', '%s');                
                            """ % (user_info['vk_id'], user_info['first_name'], 
                                user_info['last_name'], user_info['sex'], 
                                user_info['age'], user_info['city']))
            self.conn.commit()                 
            return f'БД - данные страницы {user_info["vk_id"]}-id добавлены'
        else:    
            self.cur.execute("""
                            UPDATE person
                            SET first_name = '%s', last_name = '%s', age = '%s', city = '%s'
                            WHERE vk_id = %s;
                            """ % (user_info['first_name'], user_info['last_name'], 
                                user_info['age'], user_info['city'], user_info['vk_id']))
            self.conn.commit()                 
            return f'БД - данные страницы {user_info["vk_id"]}-id обновлены'   

    def outputs_list(self, vk_id: int) -> str:
        'Выводит список избранных людей'
        with self.conn.cursor() as cur: 
            cur.execute("""
                        SELECT vk_id, first_name, last_name
                        FROM   person
                        JOIN selected ON favorite_id = vk_id
                        WHERE  elector_id = %s;
                        """% (vk_id,))
            return cur.fetchall()

    def add_photo(self, person_id: int, link_photo: str)-> str:
        self.cur.execute("""
                        INSERT INTO best_photo (person_id, link_photo) 
                        VALUES ('%s', '%s');                
                        """ % (person_id, link_photo))
        self.conn.commit()    
        return f'БД - фото добавлено'

    def add_favorite(self, elector_id: int, favorite_info: dict, photo_list: list) -> str:
        'Добавить страницу в список избранных'
        flag = self.checking_selected(elector_id, favorite_info['vk_id'])        
        if not flag:         
            print(self.add_person(favorite_info))
            for link in photo_list:
                    print(self.add_photo(favorite_info['vk_id'], link)) 
            self.cur.execute("""
                            INSERT INTO selected (elector_id, favorite_id) 
                            VALUES ('%s', '%s');                
                            """ % (elector_id, favorite_info["vk_id"]))
            self.conn.commit()                 
            return f'БД - страница {favorite_info["vk_id"]}-id добавлена к избранным'
        else:
            return f'БД - ошибка! Страница {favorite_info["vk_id"]}-id уже есть в избранных'

