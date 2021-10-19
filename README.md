# bookstore

### Install dependencies for Linux
Install psycopg2 instead of ~~psycopg2-binary~~ for Windows
```shell
pip install --upgrade pip
pip install django
pip install djangorestframework
pip install psycopg2-binary
pip install social-auth-app-django
pip install django-filter
```
### Install postgresql for Ubuntu. For [Manjaro](https://gist.github.com/marcorichetta/af0201a74f8185626c0223836cd79cfa)
```shell
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql
```
### Create database and user
```
CREATE DATABASE myproject;
CREATE USER myprojectuser WITH PASSWORD 'password';
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
\q
```
### Create the administrator
```shell
cd books
```
```shell
./manage.py createsuperuser
```
### Start migrations
```shell
./manage.py migrate
```
### Start server
```shell
./manage.py runserver
```
### Check your browser 
>[books](http://127.0.0.1:8000/book/?format=json)
### Registrate from GitHub
[auth](http://127.0.0.1:8000/auth)
### Add some books
>[admin](http://127.0.0.1:8000/admin)

and check 'books' again

