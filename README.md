Учебный репозиторий.
Плюс подсказки и гайды для себя.

<h1>СОздание базы Postgres:

<h2>psql
<p>CREATE USER %user% WITH PASSWORD '$$$$';
<p>CREATE DATABASE %dbname% OWNER %user%;
<p>ALTER USER %user% CREATEDB;
<p>\q
<p>pip install psycopg2
<p>python manage.py makemigrations
<p>python manage.py migrate
<p>python manage.py createsuperuser
