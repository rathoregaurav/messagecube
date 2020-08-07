# Data Parsing Backend

## Environment variables
SECRET_KEY = <secret_key>

DEBUG=True

DB_NAME = <db_name>

DB_USER = <db_user>

DB_PASSWORD = <db_password>

DB_HOST = <host_ip>

DB_PORT = 5432


##  Project setup instruction

#### create virtual environment, 

virtualenv -p python3 venv

#### install requirement files,

pip install -r requirement/local.txt


#### run project

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:port
