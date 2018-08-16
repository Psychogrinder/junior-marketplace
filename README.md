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
