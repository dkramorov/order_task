## Суть тестового задания:

- есть подготовленный тестовый проект (имитация онлайн-магазина).
- нужно клонировать репозиторий и выполнить несколько задач по доработке/правкам проекта.
- ниже дано описание сути проекта, описание обычных и расширенных задач.
- основная цель выполнения задач - максимально показать свои навыки.
- крайне желательно использовать типизацию там, где это поможет лучше воспринимать реализуемый функционал.
- так же нужно помнить, что в задачах важна не бизнес-логика, а оптимальность технической реализации.
- по возможности оптимизировать код, напрмер, для соответствия DRY-принципу.


#### Развертывание:
- в качестве СУБД используется postgresql>=9.6 + PostGIS
- окружение (miniconda) развертывается из файла environment.yml
- фикстуры находятся в data.json
- установка переменных окружения - через файл .env
- пример .env:
```    
B3_DB_HOST=192.168.56.104 # ip БД-сервера
B3_DB_PORT=5433 # port БД-сервера
B3_DB_NAME=order_task # имя БД
B3_DB_USER=order_task # юзер БД
B3_DB_PASSWORD=order_task # пароль БД

B3_MEDIA_ROOT=/opt/media # папка с пользовательскими данными
B3_STATIC_ROOT=/opt/static # папка со статикой

```

## Бизнес-логика:

- есть магазин и его сотрудники
- в магазине есть набор товаров
- есть набор организаций-клиентов, которые через своих представителей могут приобретать товары
- товары приобретаются посредством формирования заказов
- заказ состоит из позиций
- позицию заказа формируют товар и его кол-во
- заказ может быть закрыт ("отправлен") менеджером организации, тогда он становится недоступным для редактирования, при этом, он становится виден сотрудникам магазина


### Пользовательские роли в системе:
- админ магазина + так же является сотрудником магазина:
    - имеет доступ в админку, как суперюзер
- сотрудник магазина:
    - получение через API оформленных заказов и их позиций
- менеджер организации:
    - просмотр всех заказов и позиций своей организации
    - выполнение перевода заказа в статус "отправлен", после этого:
        - заказ нельзя редактировать
        - сотрудник магазина видит этот заказ
    - запрос аналитики (описана в задачах)
- сотрудник организации-покупателя:
    - создание/редактирование заказов и позиций заказов (без возможности "отправления" заказа)
- все роли, включая неавторизованные:
    - видят список товаров


## Задачи:

### Стандартные задачи:
1. реализовать разделение доступа к эндпоинтам на основе ролей
2. доработать состав эндпоинтов до требуемого (описание эндпоинтов - ниже)
3. при любом сохранении сущности (через веб-контекст) нужно так же сохранять:
    - юзера, который выполнял изменение (сохранение может быть как через админку, так и через API)
4. реализовать менеджер-команду для возможности выгрузки всех оформленных заказов в формате csv:
    - атрибутивный состав выгрузки:
        - название организации
        - перечень позиций (название товара, кол-во) через запятую
        - общая стоимость
5. исправить ошибку админки: /admin/customer/organization/add/
6. настроить разделы админки:
  - добавить в список читабельные поля
  - добавить поиск по текстовым полям
  - в раздел "товары" добавить поиск по диапазону цен
7. собрать минимальный docker-compose:
    - загрузка фикстур
    - подключение к БД
    - выполнение миграци
    - сборка статики
    - запуск django-сервера - runserver

### Расширенные задачи:
8. нужно хранить историю изменений позиций заказов:
    - реализовать работу с историей через класс-дескриптор к отслеживаемой модели
9. написать работу с веб-сокетами по асинхронному протоколу:
    - уведомлять менедрежа организации об изменении/создании позиций заказа
10. в задаче выгрузки заказов через менеджер-команду:
    - добавить в выгрузку расстояние между организацией и магазином (по прямой, в км)
        - для этого нужно определить параметр точки расположения магазина (например, в переменных окружения)
        - расстояние нужно получить средствами sql, вариант обсчитывать каждую отдельную запись через python не подойдет)
    - интегрировать возможность запуска и получения файла через админку


## Варианты эндпоинтов:

#### Список товаров:

- атрибуты:
    - название
    - стоимость
- фильтры:
    - полнотекстовой поиск (артикул, название)
    - фильтр по ценнику (диапазон цен)
- пагинация:
    - на странице 20 элементов
- доступность:
    - всем

#### Заказы:

- атрибуты:
    - позиции:
        - для list: список id
        - для detail: список структур
    - связанные товары (через позиции) - названия через запятую
    - общая стоимость - расчетное поле
    - статус - только на чтение
    - автор создания - только на чтение
    - автор изменения - только на чтение
    - дата/время создания - только на чтение
    - дата/время оформаления - только на чтение
- пагинация:
    - на странице 20 элементов
- доступность:
    - для сотрудника организации-покупателя:
        - создание/просмотр
    - для владельца организации-покупателя:
        - просмотр
        - спец. действие перевода заказа в статус "отправлен"
    - для сотрудника магазина:
        - просмотр (только для оформленных заказов)

#### Позиция заказа:

- атрибуты:
    - id заказа
    - кол-во единиц товара
    - id товара - на запись только при создании, после этого - только на чтение
    - общая стоимость позиции - расчетное поле
    - автор создания - только на чтение
    - автор изменения - только на чтение
    - дата/время создания - только на чтение
    - дата/время изменения - только на чтение
    - название товара - только на чтение
- пагинация:
    - список должен выводится всегда полный и только для конкретного заказа
- доступность:
    - для сотрудника организации-покупателя:
        - создание/редактирование/просмотр/удаление
    - для владельца организации-покупателя:
        - просмотр
    - для сотрудника магазина:
        - просмотр (только для оформленных заказов)

#### Аналитика по конкретной орагнизации-покупателю:

- состав:
    - кол-во заказов по датам
    - кол-во созданных/отредактированных позиций по каждому сотруднику его организации
- доступность:
    - для владельца организации-покупателя:
        - просмотр

