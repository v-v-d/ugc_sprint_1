![tests](https://github.com/v-v-d/ugc_sprint_1/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/v-v-d/ugc_sprint_1/branch/main/graph/badge.svg?token=Q8NOGB813N)](https://codecov.io/gh/v-v-d/ugc_sprint_1)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

# Cервис для хранения аналитической информации

## Ресурсы
- Доска: https://github.com/users/v-v-d/projects/3

Репозитории:
- сервис Auth API: https://github.com/v-v-d/Auth_sprint_1
- сервис Movies API: https://github.com/v-v-d/Async_API_sprint_1
- сервис Movies ETL: https://github.com/v-v-d/ETL
- сервис Admin panel: https://github.com/v-v-d/Admin_panel_sprint_1


## Основные сущности
- TODO

## Основные компоненты системы
- TODO

## Используемые технологии
- TODO

## Нагрузочное тестирование
### PostgreSQL (10 млн записей)
- Запись в базу данных: 55 секунд
- Поиск по БД (100 запросов):51 секунда

### Clickhouse
- Запись в базу данных: 14 секунд
- Поиск по БД (100 запросов): 0.12 секунд

## Работа с проектом
### Запуск
1. Создать общую сеть для всех проектов практикума, чтобы была связь между всеми контейнерами курса
```shell
docker network create yandex
```
2. Собрать и запустить текущий проект
```shell
docker-compose up --build
```
3. TODO

### Тестирование
Собрать тестовое окружение и запустить тесты
```shell
docker-compose -f docker-compose.test.yaml up --build --exit-code-from sut
```
