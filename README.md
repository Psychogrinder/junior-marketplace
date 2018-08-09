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

Для локального использования, добавить блок `ports` и вытащить наружу порт
базы данных.

### marketplace.nginx

Front-сервер для обслуживания домена.
