## Древовидное меню ##

# Запуск проекта

1. Клонируйте репозиторий:

```
git clone https://github.com/iMaanick/UpTrader.git
```

2. Активируйте виртуальное окружение:


3. Установите зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

4. Выполните миграции:

```
python manage.py migrate
```

5. Создайте суперюзера:

```
python manage.py createsuperuser
```

6. Выполните команду для заполнения тестовыми данными:

```
python manage.py create_menus
```
7. В папке с файлом manage.py запустите сервер, выполнив команду:

```
python manage.py runserver
```