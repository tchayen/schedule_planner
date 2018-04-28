# schedule planner
Python classes assignment.

*Work in progress*

App for viewing current schedule of a student, handling classes that are moved permanently, happen every N weeks, are moved occasionally and so on.

## Running
Just like a regular Django app:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

## Roadmap
- ~~setup the Django project~~
- ~~create and connect to the database~~
- ~~create basic models~~
- ~~display calendar properly~~
- ~~add username/password authentication~~
- ~~create fixture containing realistic data~~
- ~~add admin panel for managing change requests~~
- handle accept/decline buttons (maybe using csrf for safety?)
- ...

## Database
*NOTE: migrations are not version controlled*

In case you are missing some of those:
```bash
sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
```

Now you can create the database:
```bash
# Login into PostgreSQL shell
sudo su - postgres
psql

# Create the database and user
CREATE DATABASE schedule_planner;
CREATE USER schedule_planner_user WITH PASSWORD 'schedule_planner_password';

# Setup user
ALTER ROLE schedule_planner_user SET client_encoding TO 'utf8';
ALTER ROLE schedule_planner_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE schedule_planner_user SET timezone TO 'UTC';

# Give the user all privileges
GRANT ALL PRIVILEGES ON DATABASE schedule_planner TO schedule_planner_user;

# Quit
\q
exit
```

Make sure you've installed both Django and psycop2 (the latter is not installed by default and is required to connect to the PostgreSQL database)
```
pip install django psycopg2
```

## Utilities
Show git stats (i.e. number of lines added/removed per file and global summary) from the initial commit until now:
```bash
git diff --stat d28d9970 HEAD
```

Create Django superuser:
```bash
python3 manage.py createsuperuser
```