# Django Shop Project

Учебный проект интернет-магазина на Django.

##  Технологии
- Python 3.12+
- Django 4.2.27
- SQLite (по умолчанию)

##  Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/editanaks-ops/django_shop_project.git
cd django_shop_project
2. Создать виртуальное окружение
bash
Kopier kode
python -m venv .venv
Активировать его:

Windows (PowerShell):

bash
Kopier kode
.venv\Scripts\Activate.ps1
Windows (cmd):

bash
Kopier kode
.venv\Scripts\activate.bat
macOS / Linux:

bash
Kopier kode
source .venv/bin/activate
3. Установить зависимости
bash
Kopier kode
pip install -r requirements.txt
4. Применить миграции
bash
Kopier kode
python manage.py migrate
5. Создать суперпользователя (для админки)
bash
Kopier kode
python manage.py createsuperuser
6. Запустить сервер
bash
Kopier kode
python manage.py runserver
Открыть в браузере:

Сайт: http://127.0.0.1:8000/

Админка: http://127.0.0.1:8000/admin/

 Функциональность (модели)
Category — категории товаров (с вложенностью)

Product — товары (цена, остаток, описание)

Order — заказы пользователя

OrderItem — позиции в заказе

Review — отзывы пользователей (1 отзыв на товар от пользователя)

 Примечание
Файл requirements.txt содержит точные версии зависимостей проекта.
