# Командный проект по курсу «Профессиональная работа с Python»
![Иллюстрация к проекту](https://github.com/romariotrain/adpy-team8-diplom/raw/main/image/logo.png)
## Tinder на минималках

### Цель проекта

Цель командного проекта - разработать программу-бота для взаимодействия с базами данных социальной сети. Бот будет предлагать различные варианты людей для знакомств в социальной сети Вконтакте в виде диалога с пользователем.

------

### Описание работы с программой

**Программный продукт «Tinder на минималках»** - является чат ботом для сайта Вконтакте, выполняющим функцию подбора кандидатур для возможного знакомства с противоположным полом. Для функционирования чат бота программа должна быть запущена на компьютере с доступом в интернет, либо развернута на каком либо веб сервере.
Поиск кандидатур для знакомства осуществляется в сообщениях пользователя с одноименной группой Вконтакте «Tinder на минималках».

Для начала работы с чат ботом необходимо написать в сообщении группе `«привет»`. В ответ чат бот предложит написать слово `«start»` для запуска поиска кандидатур. При некорректном вводе команд, чат бот сообщает, что не понял команду. При вводе слова `«start»` чат бот выдает приветственное сообщение и предлагает нажать кнопку `«Найти пару»`.


После нажатия кнопки программа производит поиск кандидатур по следующим параметрам:
* **Пол** — противоположный полу пользователя чат ботом
* **Возраст** — при условии, что поиск кандидатур производит пользователь женского пола, в список выдачи попадают мужчины ровесники пользователя и старше пользователя (но не больше чем на пять лет). При условии, что поиск производит пользователь мужского пола, в список выдачи попадают женщины ровесники пользователя и младше пользователя (но не более чем на пять лет). 
* **Город** — подбираются кандидаты, у которых в профиле в поле город проживания указан тот же город, что и у пользователя чат ботом. Отсеиваются кандидаты родившиеся в требуемом городе, но не проживающие в нем на момент поиска.
* Так же при поиске производится отсеивание Кандидатов с закрытым профилем, с закрытой информацией о городе проживания и о дате рождения.


Вывод кандидатур осуществляется по одному, в сообщениях, cначала выводится три фотографии пользователя (при наличии), оцененные максимальным количеством лайков. Далее выводится информация о кандидате `имя`, `фамилия` и `возраст`. Отдельной строкой сообщения выводится ссылка на профиль кандидата.

Далее чат бот предлагает выбрать команду (нажатием кнопки) из четырех возможных.
Команда `«Добавить в избранное»` производит сохранение информации о кандидате в базу данных.
Команда `«Показать список избранного»` выведет информацию о кандидатах, ранее добавленных в базу данных.
Команда `«Продолжить поиск»` показывает результаты поиска следующего кандидата.
Команда `«Закончить работу»` прощается с пользователем и завершает поиск кандидатов для данного пользователя.

Для повторного запуска чат бота необходимо заново написать в поле сообщений `«привет»`.

---
### Описание модулей программы.
Программа «Tinder на минималках» состоит из пяти модулей: `main.py`, `vk_bot.py`, `db_postgresql.py`, `api_vk.py` и `config.py`

* Модуль `main.py` — запускает работу программы, запускает создание базы данных, необходимых таблиц и запускает модуль vk_bot.py
* Модуль `vk_bot.py` — служит для взаимодействия пользователя с ботом, обрабатывает запросы пользователя, выдает результаты работы программы в чат пользователю.
* Модуль `api_vk.py` — взаимодействует с API Вконтакте, осуществляет поиск и отбор кандидатов и информации, отбор фотографий по заданным критериям.
* Модуль `db_postgresql.py` — выполняет всю работу с базой данных, создание базы, создание таблиц, запись информации в базу данных, чтение информации из базы данных.
* Модуль `config.py` — выполняет роль хранилища настроек программы, токены для доступа к API ВК, пароль для базы данных.
