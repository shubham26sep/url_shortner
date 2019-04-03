URL Shortner
=========

# Installation

## Install OS (Ubuntu) Requirements

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install vim-gnome build-essential git-core python-dev python-virtualenv supervisor
    sudo apt-get install git gcc python-dev python-setuptools libjpeg-dev zlib1g-dev libpq-dev

## Clone Project

    git clone <repository> url_shortner

## Virtual Envirnoment and requirements

    virtualenv -p /path/to/python3.5 venv
    source venv/bin/activate
    pip install -r requirements.txt

## Postgres setup

    pip install psycopg2
    sudo su - postgres
    psql -d template1 -U postgres
    CREATE USER your-username WITH PASSWORD your-password;
    ALTER USER your-username WITH SUPERUSER;
    CREATE DATABASE db_name;
    ALTER ROLE admin SET client_encoding TO 'utf8';
    ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
    ALTER ROLE admin SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE db_name TO your-username;
    \q
    psql -d mu_db -U your-username

## Add postgresql database settings in DATABASE settings in config/settings.py

## Create a superuser account.

    python manage.py createsuperuser

## Running Development Server

    python manage.py runserver

**Note:** Never forget to enable virtual environment (`source venv/bin/activate`) before running above command and use settings accordingly.
