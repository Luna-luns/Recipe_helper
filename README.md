![Foodgram Workflow Status](https://github.com/xofmdo/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Продуктовый помощник Foodgram 

## Технологии

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)


## Описание проекта Foodgram
Приложение "Продуктовый помощник» представляет собой сервис, на котором пользователи публикуют рецепты, имеют возможность
подписаться на публикации других авторов. 
Вы сможете добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Запуск проекта в dev-режиме

- Клонируйте репозиторий с проектом на свой компьютер
```bash
git clone https://github.com/Luna-luns/Foodgram.git
```

- Установите и активируйте виртуальное окружение

```bash
source /venv/bin/activate
```

- Установите зависимости из файла requirements.txt

```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```
- Создате файл .env в папке проекта. Пример:
```.env
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

### Выполните миграции и создайте суперпользователя:
```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```

### Загрузите статику:
```bash
python3 manage.py collectstatic --no-input
```
### Заполните базу тестовыми данными: 
```bash
python3 manage.py upload_data
python3 manage.py upload_tags
```


## Запуск проекта через Docker

Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). 

Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

Клонируйте репозиторий с проектом на свой компьютер:
```bash
git clone https://github.com/Luna-luns/foodgram-project-react.git
```

- в Docker cоздайте образ :
```bash
docker build -t foodgram .
```

Соберите контейнеры:
```bash
cd ../infra
docker-compose up -d --build
```

### Выполните миграции:
```bash
docker-compose exec backend python3 manage.py migrate
```
### Создайте суперпользователя:
```bash
docker-compose exec backend python3 manage.py createsuperuser
```

### Загрузите статику:
```bash
docker-compose exec backend python3 manage.py collectstatic --no-input
```

### Заполните базу тестовыми данными:
```bash
docker-compose exec backend python3 manage.py upload_data.py
docker-compose exec backend python3 manage.py upload_tags.py  
```

### IP сервера:
```bash
158.160.114.76
```

### Логин и пароль администратора:
```bash
admin5
admin12345
```

## 🚀 Обо мне

Начинающий backend-разработчик на Python
- [@Елизавета Струнникова](https://github.com/Luna-luns)
  
## Обратная связь

Email: liza.strunnikova@yandex.ru<br>
Telegram: @l_lans
