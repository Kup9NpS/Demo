Учебный репозиторий.
Плюс подсказки и гайды для себя.

<h1>СОздание базы Postgres:</h1>

<h2>psql</h2>
<p>CREATE USER %user% WITH PASSWORD '$$$$';</p>
<p>CREATE DATABASE %dbname% OWNER %user%;</p>
<p>ALTER USER %user% CREATEDB;</p>
<p>\q</p>
<p>pip install psycopg2</p>
<p>python manage.py makemigrations</p>
<p>python manage.py migrate</p>
<p>python manage.py createsuperuser</p>
