# Linc Local Backend

> “The beginning of wisdom is to call things by their proper name.” ― Confucius


## How to get on board

1. Create a Python v3.11 virtual environment (and start it)

* `$ python3.11 -m venv .venv --prompt DjangoApp`

* `$ source .venv/bin/activate`

2. Install all required packages

* `$ pip install -r requirements/dev.txt`

3. Create your own .env file that corresponds to /settings/dev.py

```
DB_NAME=<name-of-database>
DB_HOST=localhost
DB_PORT=5432
DB_USER=<your-db-username>
DB_PASSWORD=<your-db-password>
DB_SECRET=<the-django-secret-key>
```

4. Committing migrations for database modification

* `$ make dev-makemigrations`

5. Apply migrations to the database

* `$ make dev-migrate`

6. Start Django server

* `$ make dev-start`
