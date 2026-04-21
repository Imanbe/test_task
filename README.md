# Инструкция по запуску
    1. в .env вставить токен бота
    2. make up
    3. make fill (заполнение бд тестовыми данными)

# Команды бота
    1. /create_user
    2. /delete_user
    3. /list_users

# Makefile команды:
    1. make up - запуск контейнеров
    2. make down - удаление контейнеров с volume
    3. make logs - просмотр логов
    4. make fill - генерация 1000 тестовых пользователей
    5. make format - форматирование кода Ruff
    6. make lint - проверка кода линтером Ruff