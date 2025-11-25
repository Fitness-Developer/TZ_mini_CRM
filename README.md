# Тестовое задание 
# "Создание mini-CRM" распределения лидов между операторами по источникам

Стэк проекта:
- FastAPI
- SQLite
- SQLalchemy
- pydantic

## Структура проекта

```
app/
 ├─ main.py          # Точка входа FastAPI
 ├─ models.py        # SQLAlchemy модели
 ├─ schemas.py       # Pydantic-схемы
 ├─ utils.py         # Логика распределения операторов
 └─ database.py      # Подключение к БД, SessionLocal, Base
crm.db               # SQLite база данных (создаётся автоматически)
requirements.txt
README.md
```

## Установка и запуск
```
git clone https://github.com/Fitness-Developer/TZ_mini_CRM.git
cd TZ_mini_CRM
```
## Создание виртуального окружения (опционально, если нужно)
```
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows
```
## Установка зависимостей
```
pip install -r requirements.txt
```
## Запуск приложения
```
uvicorn app.main:app --reload
```
Доступ к API - http://127.0.0.1:8000/docs

Основное описание структуры проекта находится в файлах, там написан функционал и что для чего нужно.

## Основные сущности
### Оператор (Operator)
- активность: может/не может принимать обращения
- лимит нагрузки
- связь с источниками (вес распределения)
### Лид (Lead)
- уникальный внешний ID (телефон/email/любой идентификатор)
- несколько обращений из разных источников
### Источник (Source)
- канал/бот
- список операторов + вес распределения
### Обращение (Contact)
- факт входящего сообщения
- автоматически выбирается оператор
