# Дипломный проект Я.Практикума

[![Foodgram Workflow](https://github.com/sonoffjord/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)](https://github.com/sonoffjord/foodgram-project-react/actions/workflows/foodgram.yml)
------------------------
## О проекте
 
**Foodgram** сервис где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

**Страница проекта**: [Клац](http://178.154.226.189/signin)

**Страница API**: [Клац](http://178.154.226.189/api/docs/)


------------------------

## Запуск проекта
Склонируйте репозиторий на рабочий сервер командой https://github.com/sonoffjord/foodgram-project-react.git,
в каталоге создайте файл `.env` и заполните переменные, после чего из каталога 
`./infra` запустите контейнеры: `docker-compose up -d.`

**Переменные** `.env`**:**
- `SECRET_KEY` - секретный ключ Django
- `HOSTNAME` - список доменов, на которых будет развёрнут сайт
- `DB_HOST` - название контейнера БД
- `DB_PORT` - порт БД (используется Postgresql: по умолчанию - 5432)
- `DB_NAME` - название БД
- `POSTGRES_PASSWORD` - пароль от БД
- `POSTGRES_USER` - логин БД
**Git Secrets**
- `HOST` - адрес удаленного сервера
- `USER` - логин удаленного сервера
- `SSH_KEY` - приватный SSH ключ
- `PASSPHRASE` - защитная фраза SSH ключа (если есть)


## Инструменты в проекте
![Python](https://img.shields.io/static/v1?style=flat&message=Python&color=5a5a5a&logo=Python&logoColor=FFFFFF&label=)
![Django](https://img.shields.io/static/v1?style=flat&message=Django&color=5a5a5a&logo=Django&logoColor=FFFFFF&label=)
![NGINX](https://img.shields.io/static/v1?style=flat&message=NGINX&color=5a5a5a&logo=NGINX&logoColor=FFFFFF&label=)
![PostgreSQL](https://img.shields.io/static/v1?style=flat&message=PostgreSQL&color=5a5a5a&logo=PostgreSQL&logoColor=FFFFFF&label=)
![Docker](https://img.shields.io/static/v1?style=flat&message=Docker&color=5a5a5a&logo=Docker&logoColor=FFFFFF&label=)
