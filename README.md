# Django Catalog Project

Проект интернет-магазина на Django с каталогом товаров.

## Функциональность

- Главная страница
- Каталог товаров
- Страница контактов
- Адаптивный дизайн с Bootstrap

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd django_catalog_project

2. Создайте виртуальное окружение:
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Установите зависимости:
bash
pip install -r requirements.txt

4.Примените миграции:

bash
python manage.py migrate

5.Запустите сервер:

bash
python manage.py runserver