Учебный репозиторий.
Плюс подсказки и гайды для себя.

СОздание базы Postgres:

psql
CREATE USER %user% WITH PASSWORD '$$$$';
CREATE DATABASE %dbname% OWNER %user%;
ALTER USER %user% CREATEDB;
\q
pip install psycopg2
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
