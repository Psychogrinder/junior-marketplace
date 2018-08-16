# Проект маркетплейса

## Описание сервисов

### marketplace.app

Основное приложение маркетплейса: API + frontend

### marketplace.db

Сервис базы данных. Postgres 10

#### Запуск

Перейти в директорию ./marketplace.db и выполнить
```
docker-compose up -d
```

Перейти в корневую директорию и выполнить 
```
bin/create_virtualenv.sh
```

После выполнить 
```
bin/run-flask-app.sh или bin/init_db_and_run.sh
```

### marketplace.nginx

Front-сервер для обслуживания домена.

### marketplace.app/marketplace/utils/create-content.py
Скрипт для наполнения уже созданной базы данных. Убедитесь что Flask не запущен,
а docker с базой данных запущен.

В папке utils выполните в терминале команды:
export FLASK_APP=models.py
flask run
python3 create_content.py

