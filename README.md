# Тестовое задание для VictoryGroup


    Этот проект представляет собой API,часть backend-приложения для поиска авиабилетов.
    Состоит приложение из авторизации, поиска авиабилетов и отображения подробных данных
    по билету.

   
    

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Документация](#документация)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)

## Технологии
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLalchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [OpenAPI](https://www.openapis.org/)


## Использование
Клонируйте репозиторий на локальную машину:
```sh
$ git clone https://github.com/advatroniks/task-python
```

Перейдите в папку с проектом:
```sh
$ cd /task-python
```

Выполнитье команды Docker.
```docker
$ sudo docker compose up
```

## Документация
> Использование API

    После запуска интерактивния документация доступна по адресу 
    http://127.0.0.1:8080/docs#/ Реализовано через OpenAPI(Swagger)
    
    ===============================AuthModule====================================

    *Регистрация пользователя по средством ввода(Email, password)
    *Аутентификация пользователя по протоколу Oauth2(JWT Token)
    


    ==============================TicketsModule===================================

    1)Поиск авиабилетов при ОБЯЗАТЕЛЬНОМ указании даты вылета, аэропорта вылета и 
    аэропорта прилета. 
    >>>>>>>>>>>>>>>>>>>>>>>Указывается КОД АЭРОПОРТА СОГЛАСНО СТАНДАРТУ ICAO
    (https://tst-cargo.ru/faq/spisok-aeroportov-rossii-s-kodami/)
    >>>>>>>>>>>>>>>>>>>>>>>Дата вылета указывается по формату ISO 8601(YYYY-MM-DD)
    2)В зависимости от параметров:
        =>> cheapest > сортировка по самому дешевому билету(по умолчанию)
        =>> nearest > сортировка по ближайшему билету
    3)Если на текущую дату нет прямого рейса, то ищется билет с пересадками(
    ограничение количество пересадок определяется днем вылета) прим.
    *2023-12-12 USPP > UUDD (Пермь-Мск) нет прямых рейсов
    *Алгортим ищет все возможные связи, через которые можно долететь в UUDD
    *Выбирает самый дешевый вариант, несколько связных билетов.


>Генерация Данных
    
    При генерации данных используются скрипты, расположенные /src/geneate_data.
    Для генерации данных запустить В СТОГОМ ПОРЯДКЕ УКАЗАННОМ НИЖЕ!


```sh
$ python3 src/generate_data/airports/service.py
```
```sh
$ python3 src/generate_data/flights/service.py  
```
```sh
$ python3 src/generate_data/tickets/service.py
```

    Параметры для генерации задаются в файле utils.py. Подробное описание см. в файле
    в DockStrings для функций.

>Схема Базы Данных

>![alt text](https://i.ibb.co/ZNR9gB3/database-schema.jpg)

>Сущность flights

    *departure_airport(PK) - аэропорт вылета,
    *arrival_airport(FK) - аэропорт прилета,
    *scheduled_departure(FK) - время вылета по плану,
    *scheduled_arrival - время прилета по плану
    ВРЕМЯ УКАЗАНО СОГЛАСНО UTC!!! без учета локалоного часового поясаэ

>Сущность tickets

    *id(PK) - уникальный идентификатор билета
    *price - цена, для упрощения без учета десятичных долей и валюты
    *flight_no(FK) - номер рейса
    *fare_condition - класс обслуживания(economy, business, first)

>Сущность airports

    *city - город СОГЛАСНО СТАНДАРТУ ISO 3166(https://ru.wikipedia.org/wiki/ISO_3166)
    *airport_name - Название аэропорта ЛАТИНИЦЕЙ
    *icao_code(PK) - стандарт ICAO (https://tst-cargo.ru/faq/spisok-aeroportov-rossii-s-kodami/)

>Сущность users

    *id(PK) - уникальный идентификатор UUID
    *email - email пользователя указанные при регистрации
    *hashed_password - хэш пароля согласно SHA-256


## To do
- [x] Основной функционал
- [ ] Генерация реальных данных


## Команда проекта
- [Advatrnoiks](t.me/advatroniks) tixxx333@yandex.ru — Back-End Engineer
