# schedule planner
Python classes assignment.

App for viewing current schedule of a student, handling classes that are moved permanently, happen every N weeks, are moved occasionally and so on.

**WIP**

## Running
Just as a regular Django app
```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

## Roadmap
- display calendar
- add username/password authentication

## Recurring events system

### tests
- 04-01 - 06-01 11:15, regular
- 04-01 - 06-01 12:50, moved to 16:15 on 05-01, same day
- 04-01 - 06-01 08:00 every 2w

## Database
*NOTE: migrations are not version controlled*

## Development config
Mostly useful for me, but trying those values might help if something does not work.

### database
```bash
schedule_planner          # database name
schedule_planner_user     # username
schedule_planner_password # password
```

### superuser
```bash
admin                     # username
adminadmin                # password
```
