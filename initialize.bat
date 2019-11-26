del account\migrations\0001_initial.py
del appointments\migrations\0001_initial.py
del boards\migrations\0001_initial.py
del survey\migrations\0001_initial.py
del db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py custom_migrations
python manage.py exampleDB