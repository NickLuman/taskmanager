# Taskmanager service

# Содержание:

* [ТЗ](#technical-task)
  + [Технологические требования](#technological-requirements)
  + [Функциональные требования](#functional-requirements)
* [Описание API](#description-api)
  + [Реализация](#implementation)
  + [Пояснения по реализации API](#explanations)
* [Сборка и запуск](#assembling-and-launch)
* [Определение степени покрытия приложения тестами](#test-coverage)
* [Пример взаимодействия с API с помощью curl](#curl-interaction)
  + [Создание пользователя](#user-creation)
  + [Получение токена (авторизация)](#getting-token)
  + [Добавление задачи](#adding-task)
  + [Получение задачи](#getting-task)
  + [Изменение параметров задачи](#changing-task)
  + [Получение списка задач](#getting-task-list)
  + [Получение списка с фильтрацией задач](#getting-task-list-filtration)
  + [Получение списка изменений конкретной задачи](#getting-list-task-changing)
  + [Удаление задачи](#deletion-task)

## ТЗ <a name="technical-task"></a>:
---
* Требуется написать персонализированный сервис task manager, позволяющий пользователю ставить себе задачи, отражать в системе изменение их статуса и просматривать историю задач.

### Технологические требования <a name="technological-requirements"></a>:

* Сервис должен быть написан на python3 с использованием любого веб-фреймворка (Django, flask, aiohttp…) 
* Сервис должен хранить данные в реляционной базе данных (postgresql, mysql) 
* Сервис должен предоставлять интерфейс в виде JSON API, это единственный способ общения клиента с сервисом 
* Авторизация в апи происходит с помощью токена (переданного в заголовке Authorization) 

#### Дополнения:

* Сервис будет покрыт тестами 
* Сервис будет содержать Dockerfile для сборки сервиса 
* Подробный README с описанием реализованного API и пояснениями как именно реализуются нижеприведённые функциональные требования 

### Функциональные требования <a name="functional-requirements"></a>:

* Пользователь может зарегистрироваться в сервисе задав пару логин-пароль 
* В системе может существовать много пользователей 
* Пользователь может авторизоваться в сервисе предоставив пару логин-пароль и получив в ответе токен 
* Пользователь видит только свои задачи 
* Пользователь может создать себе задачу. Задача должна как минимум содержать следующие данные:

### (\*) - обязательные поля

1. \*Название
2. \*Описание
3. \*Время создания
4. \*Статус - один из Новая, Запланированная, в Работе, Завершённая
5. Планируемая дата завершения

* Пользователь может менять статус задачи на любой из данного набора 
* Пользователь может менять планируемое время завершения, название и описание 
* Пользователь может получить список своих задач, с возможностью фильтрации по статусу и планируемому времени завершения 

#### Дополнения:

* Возможность просмотреть историю изменений задачи (названия, описания, статуса, времени завершения)

## Описание API <a name="description-api"></a>:
---
### Реализация <a name="implementation"></a>:

* Сервис написан на python3 с использованием веб-фреймворка Django. Данные хранятся в postgresql.
* Добавлена возможность сборки и запуска проекта через docker-compose.
* Приложение task покрыто тестами на ~90%.
* В системе может существовать много пользователей. Регистрация новых происходит по адресу: 
localhost:8000/api/signup/
* Зарегистрированный пользователь может получить токен авторизации по адресу: 
localhost:8000/api/login/
* Пользователь видит только свои задачи. Осуществлен функционал CRUD для пользователя. Для работы с сервисом необходимо при каждой манипуляции с данными передавать токен пользователя в заголовке запроса.
* Обращение к задачам происходит по их id в БД. Пример: localhost:8000/api/task/id. При успешном создании задачи, будет возвращен URL для доступа к задаче.
* Пользователь может изменять статус задачи на любой из (new/planned/in progress/done), также можно изменить параметры: title, description, completion (Время и дата выполнения задачи).
* Добавлена возможность фильтрации списка всех задач по статусу и/или планируемому времени завершения. Когда делаем GET-запрос по адресу localhost:8000/api/all/ необходимо в тело запроса добавить параметры -
  + filter_by_status='new/planned/in progress/done'
  и/или
  + filter_by_completion='dateTtime'
* Существует возможность просмотра истории всех изменений задачи (реализована дополнительная модель TaskChange Many-to-One к Task): Прим просмотр изменения задачи по id 1 - localhost:8000/api/task/1/changes

### Пояснения по реализации API <a name="explanations"></a>:
* Пользователь может зарегистрироваться в сервисе задав пару логин-пароль
  + По дефолтной модели - User, определенной в Django, был написан сериализатор - UserSerializer. В данном классе переопределен метод - create, c помощью которого и происходит регистрация. После передачи валидных данных POST запросом по URL localhost:8000/api/signup/ {username, password}, происходит создание объекта User с его уникальным токеном в БД.

* В системе может существовать много пользователей 
  + В отдельной таблице БД, определенной как User, может содержаться N-е количество пользователей.

* Пользователь может авторизоваться в сервисе предоставив пару логин-пароль и получив в ответе токен
  + После передачи валидных данных POST запросом по URL localhost:8000/api/login/  {username, password}, пользователь получает свой уникальный токен для дальнейшего взаимодействия с API.

* Пользователь видит только свои задачи 
  + Любое взаимодействие с данными (просмотр всех задач, изменений, функционал CRUD), происходит только с помощью переданного в заголовке Authorization - токена. Прим {Authorization: Token a80924fqj20jq39f240f42}, в противном случае запрос будет отклонен. Все это осуществляется с помощью дефолтных декораторов DRF: @authentication_classes, @permission_classes. Они определяют параметры доступа к ViewSet, и в данном случае только у авторизованных пользователей есть доступ ТОЛЬКО к ИХ данным.

* Пользователь может создать себе задачу. Задача должна как минимум содержать следующие данные:

  (\*) - обязательные поля

  1. \*Название
  2. \*Описание
  3. \*Время создания
  4. \*Статус - один из Новая, Запланированная, в Работе, Завершённая
  5. Планируемая дата завершения

  + В models описана модель Task - со следующими параметрами: 
    - user: Пользователь, которому принадлежит задача (связь OtM), 
    - title: Название задачи. *
    - description: Описание задачи. *
    - created: Дата и время появления задачи.
    - updated: Дата и время обновления задачи.
    - status: Статус задачи, возможны только позиции: new, planned, in progress, done. (при создании объекта без указания статуса по умолчанию - new) *
    - completeion: Планируемая дата завершения. 

    Также в serializers определен класс TaskSerializer, необходимый для передачи модели и взаимодействия с ней через API.


* Пользователь может менять статус задачи на любой из данного набора 
* Пользователь может менять планируемое время завершения, название и описание 
  + Посредством View - api_get_update_delete_task определена возможность изменения данных с помощью PUT запроса и новых переопределенных данных (не пустых, данные проходят валидацию, ввод таких же данных, что и в БД не валиден!).

* Пользователь может получить список своих задач, с возможностью фильтрации по статусу и планируемому времени завершения 
  + Внутри views view_task отвечает за порядок отображения данных, с помощью встроенных средств Django проводится фильтрация по указанным полям. 
    - filter_by_status: при заданном параметре (new/planned/in progress/done) происходит вывод задач, с соответствующей позицией status.
    - filter_by_completion: при заданном параметре (old(задачи, у которых истек срок реализации)/today/tomorrow/this month) происходит вывод задач с соответствующей позицией completion  

* Возможность просмотреть историю изменений задачи (названия, описания, статуса, времени завершения):
  + В models описана модель TaskChange - со следующими параметрами:
    - task: Задача, к которой относятся изменения (связь OtM)
    - changed_title: Запись изменений названия задачи до -> после.
    - changed_description: Запись изменений описания задачи до -> после.
    - changed_status: Запись изменений статуса задачи до -> после.
    - changed_completion: Запись изменений времени исполнения задачи до -> после.
    - changed_at: Запись времени изменения задачи.

  + С помощью View - api_get_task_changes осуществляется формирование списка изменения определенной задачи. Сначала находим задачу по ее id, после находим соответсвующие ей изменения.

## Сборка и запуск <a name="assembling-and-launch"></a>:
---
### Сборка:

* \$docker-compose build

### Делаем миграцию:

* \$docker-compose run web ./manage.py migrate

### Запуск:

* \$docker-compose up

## Определение степени покрытия приложения тестами <a name="test-coverage"></a>:
---
* \$docker-compose run web coverage run --branch --source=task ./manage.py test

* \$docker-compose run web coverage report

## Пример взаимодействия с API с помощью curl <a name="curl-interaction"></a>:
---
### Создание пользователя <a name="user-creation"></a>:

- \$curl -X POST -d "username=qwerty&password=1234test" http://localhost:8000/api/signup/

### Получение токена (авторизация) <a name="getting-token"></a>:

- \$curl -X POST -d "username=qwerty&password=1234test" http://localhost:8000/api/login/

#### Результат:

- {"token":"3bbe704c5134f42d2a80a60fa158cb43a8434c51"}

### Добавление задачи <a name="adding-task"></a>:

1. - \$curl -X POST -H "Authorization: Token 3bbe704c5134f42d2a80a60fa158cb43a8434c51" -d "title=test&description=test-d&status=new&completion=2020-10-07T18:00" http://localhost:8000/api/new/

2. - \$curl -X POST -H "Authorization: Token 3bbe704c5134f42d2a80a60fa158cb43a8434c51" -d "title=test-2&description=test-d-2&status=planned&completion=2021-10-07T18:00" http://localhost:8000/api/new/

#### Результат:

1. - {"URL":"http://localhost:8000/api/task/11"}
2. - {"URL":"http://localhost:8000/api/task/14"}

### Получение задачи <a name="getting-task"></a>:

- \$curl -X GET -H "Authorization: Token 3bbe704c5134f42d2a80a60fa158cb43a8434c51" http://localhost:8000/api/task/11

#### Результат:

{"id":11,"title":"test","description":"test-d","created":"2020-10-05T13:59:12.505248Z","status":"new","completion":"2020-10-07T18:00:00Z"}

### Изменение параметров задачи <a name="changing-task"></a>:

1. - \$curl -X PUT -H "Authorization: Token 3bbe704c5134f42d2a80a60fa158cb43a8434c51" -d "title=test-u-1&description=test-d-u-1" http://localhost:8000/api/task/11
2. - \$curl -X PUT -H "Authorization: Token 3bbe704c5134f42d2a80a60fa158cb43a8434c51" -d "status=planned&dcompletion=2020-10-08T12:00" http://localhost:8000/api/task/11

#### Pезультат:

1. - {"title":"test -> test-u-1","description":"test-d -> test-d-u-1","status":"empty/invalid format/the same data","completion":"empty/invalid format/the same data"}
2. - {"title":"empty/invalid format/the same data","description":"empty/invalid format/the same data","status":"new -> planned","completion":"2020-10-07 18:00:00+00:00 -> 2020-10-08T12:00"}

### Получение списка задач <a name="getting-task-list"></a>:

- \$curl -X GET -H "Authorization: Token 3bbe704c5134f42d2a80a60fa158cb43a8434c51" http://localhost:8000/api/all/

#### Результат:

[{"id":11,"title":"test-u-1","description":"test-d-u-1","created":"2020-10-05T13:59:12.505248Z","status":"in progress","completion":"2020-10-08T12:00:00Z"},{"id":14,"title":"test-2","description":"test-d-2","created":"2020-10-05T14:12:41.164439Z","status":"planned","completion":"2021-10-07T18:00:00Z"}]

### Получение списка с фильтрацией задач <a name="getting-task-list-filtration"></a>:

1. - \$curl -X GET -H "Authorization: Token 3bbe704c5134f42d2a80a60fa158cb43a8434c51" -d "filter_by_status=planned" http://localhost:8000/api/all/
2. - \$curl -X GET -H "Authorization: Token 3bbe704c5134f42d2a80a60fa158cb43a8434c51" -d "filter_by_completion=this week" http://localhost:8000/api/all/


#### Результат:

1. - [{"id":14,"title":"test-2","description":"test-d-2","created":"2020-10-05T14:12:41.164439Z","status":"planned","completion":"2021-10-07T18:00:00Z"}]
2. - [{"id":11,"title":"test-u-1","description":"test-d-u-1","created":"2020-10-05T13:59:12.505248Z","status":"in progress","completion":"2020-10-08T12:00:00Z"},{"id":14,"title":"test-2","description":"test-d-2","created":"2020-10-05T14:12:41.164439Z","status":"planned","completion":"2021-10-07T18:00:00Z"}]

### Получение списка изменений конкретной задачи <a name="getting-list-task-changing"></a>:

- \$curl -X GET -H "Authorization: Token 3bbe704c5134f42d2a80a60fa158cb43a8434c51" http://localhost:8000/api/task/11/changes

#### Результат:

[{"id":13,"changed_title":"No changes.","changed_description":"No changes.","changed_status":"new -> planned","changed_completion":"2020-10-07 18:00:00+00:00 -> 2020-10-08T12:00","changed_at":"2020-10-05T14:06:07.479313Z"},
{"id":12,"changed_title":"test -> test-u-1","changed_description":"test-d -> test-d-u-1","changed_status":"No changes.","changed_completion":"No changes.","changed_at":"2020-10-05T14:04:31.459897Z"}]

### Удаление задачи <a name="deletion-task"></a>:

- \$curl -X DELETE -H "Authorization: Token 3bbe704c5134f42d2a80a60fa158cb43a8434c51" http://localhost:8000/api/task/11

