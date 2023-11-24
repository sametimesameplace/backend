# SameTimeSamePlace Backend

Welcome to the SameTimeSamePlace Backend project! Our goal is to bring people together who want to experience new things and get to know new people at the same time.

## How to run

### Preparations
#### .env file
This project uses Django and PostgreSQL. Make sure you have a PostgreSQL-server running.
To run the project, clone the repo and create a `.env` file in the root folder containing:
```
DB_HOST=<address of your postgresql server>
DB_NAME=<name of the database you want to use>
DB_USER=<postgres-username>
DB_PASSWORD=<postgres-user-password>
DB_PORT=<port to connect to your server, default is 5432>
DB_SECRET=<secret token>
RAPID_API=<your geodb api token>
```
To obtain the `RAPID_API` key, you can subscribe to the [GeoDB Cities API on RapidAPI](https://rapidapi.com/wirefreethought/api/geodb-cities). Leaving the value empty will still allow the project to work, but the city information of newly created timeplaces won't be automatically filled.

To create a new secret token, you can import `secrets` in python and use `secrets.token_urlsafe(<bytes>)`. It's common to precede `django-insecure` for dev environments.

#### Python environment
Create a virtual python environment with the tool of your choice, for example `venv`:
```bash
python -m venv .venv
```
And activate it with 
```bash
source .venv/bin/activate
```

Next, install the required modules with pip:
```bash
pip install -r requirements/dev.txt
```

For convenience, the `Makefile` includes several targets - for this case, you can use 
```bash
make dev-install
```
 to install the dependencies.

#### Migrating the models to the database
To populate your database with the required tables and relations, run 
```bash
make dev-makemigrations
```
followed by 
```bash
dev-migrate
```

#### Create an admin user
To create an admin user, you can use 
```bash
python manage.py createsuperuser --settings=config.settings.dev
```

### Starting the server
You should now be able to start the django server with 
```bash
make dev-start
```
and access the site on [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

The Swagger API documentation is available on [http://127.0.0.1:8000/api/v1/swagger](http://127.0.0.1:8000/api/v1/swagger)
