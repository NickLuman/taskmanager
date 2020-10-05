# Taskmanager service

# Содержание:

1. [ТЗ](#technical-task)
   1.1 [Технологические требования](#technological-requirements)
   1.2 [Функциональные требования](#functional-requirements)
2. [Описание API](#description-api)
   2.1 [Реализация](#implementation)

## ТЗ <a name="technical-task"></a>:

- Требуется написать персонализированный сервис task manager, позволяющий пользователю ставить себе задачи, отражать в системе изменение их статуса и просматривать историю задач.

### Технологические требования <a name="technological-requirements"></a>:

- Сервис должен быть написан на python3 с использованием любого веб-фреймворка (Django, flask, aiohttp…) +
- Сервис должен хранить данные в реляционной базе данных (postgresql, mysql) +
- Сервис должен предоставлять интерфейс в виде JSON API, это единственный способ общения клиента с сервисом +
- Авторизация в апи происходит с помощью токена (переданного в заголовке Authorization) +

#### Дополнения:

- Сервис будет покрыт тестами -
- Сервис будет содержать Dockerfile для сборки сервиса +
- Подробный README с описанием реализованного API и пояснениями как именно реализуются нижеприведённые функциональные требования -

### Функциональные требования <a name="functional-requirements"></a>:

- Пользователь может зарегистрироваться в сервисе задав пару логин-пароль +
- В системе может существовать много пользователей +
- Пользователь может авторизоваться в сервисе предоставив пару логин-пароль и получив в ответе токен +
- Пользователь видит только свои задачи +
- Пользователь может создать себе задачу. Задача должна как минимум содержать следующие данные:

### (\*) - обязательные поля

1. \*Название
2. \*Описание
3. \*Время создания
4. \*Статус - один из Новая, Запланированная, в Работе, Завершённая
5. Планируемая дата завершения

- Пользователь может менять статус задачи на любой из данного набора +
- Пользователь может менять планируемое время завершения, название и описание +
- Пользователь может получить список своих задач, с возможностью фильтрации по статусу и планируемому времени завершения +

#### Дополнения:

- Возможность просмотреть историю изменений задачи (названия, описания, статуса, времени завершения) +

## Описание API <a name="description-api"></a>:

### Реализация <a name="implementation"></a>:

- Сервис написан на python3 с использованием веб-фреймворка Django. Данные хранятся в postgresql.
- Добавлена возможность сборки и запуска проекта через docker-compose.
- В системе может существовать много пользователей. Регистрация новых происходит по адресу:
  localhost:8000/api/signup/
- Зарегистрированный пользователь может получить токен авторизации по адресу:
  localhost:8000/api/login/
- Пользователь видит только свои задачи. Осуществлен функционал CRUD для пользователя. Для работы с сервисом необходимо при каждой манипуляции с данными передавать токен пользователя в заголовке запроса.
- Обращение к задачам происходит по их id в БД. Пример: localhost:8000/api/task/id. При успешном создании задачи, будет возвращен URL для доступа к задаче.
- Пользователь может изменять статус задачи на любой из (new/planned/in progress/done), также можно изменить параметры: title, description, completion (Время и дата выполнения задачи).
- Добавлена возможность фильтрации списка всех задач по статусу и/или планируемому времени завершения. Когда делаем GET-запрос по адресу localhost:8000/api/all/ необходимо в тело запроса добавить параметры -
  1.filter_by_status='new/planned/in progress/done'
  и/или
  2.filter_by_completion='dateTtime'
- Существует возможность просмотра истории всех изменений задачи (реализована дополнительная модель TaskChange Many-to-One к Task): Прим просмотр изменения задачи по id 1 - localhost:8000/api/task/1/changes
