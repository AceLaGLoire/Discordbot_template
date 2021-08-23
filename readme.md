# Ava

## How to run the bot

### First time setup
1. First create a local environment
2. Activate local environment
3. Install dependencies

### Setup
1. Activate local environment


### .env
Copy content of `example.env` to a new file called `.env` and provide you discord token. <br>
If you use sqlite than `DATABASE` should be `DATABASE=sqlite:///Database.db`. <br>
The other `DB` values can be left blank.


### Postgress datagbase
Install `docker` and `docker-compose`. <br>
Run the containers and visit adminer on `localhost:8080` <br>
you can loging with:<br>
```
System: Postgres
Server: postgres
Username: postgres
Password: password
Database: blank or database 
```

### Instructions
| instruction                  | code                                   | note | 
|------------------------------|----------------------------------------|------|
| Create a local environment   | ```python3 -m venv venv ```            | |
| Activate local environment   | ```source  venv/bin/activate ```       | |
| Deactivate local environment | ```deactivate ```                      | |
| Install dependencies         | ```pip install -r requirements.txt ``` | |
| run          containers      | ```docker-compose up -d```             | -d = detached mode   |
| stop         container       | ```docker-compose down```             |   |


### notes
#### Setup
>This bot uses `sqlite` or `postgress` as a database provider with `sqlalchemy` as
its object relational mapper `(ORM)`. While in development you may use `sqlite`.

> While installing the requirements with `pip` you may run into a problem with `psycopg2`
to resovle this make sure `postgress` is installed.  <br>
For mac: `brew install postgress` than re run dependencies. <br>
For Linux: `sudo apt install libpq-dev python3-dev` than re run dependencies.

> You can have a look at `docker-compose.yml` to find the variable sources.

> Each each time you run the bot the database wil be emptied. This insures the creation of the objects,
 to disabled this behaviour look in `/Bot/Database/__init__.py` line `30` `Base.metadata.drop_all(engine)`.


#### Database new model
> If you add a new model to the database. Be sure to import it in `Database/__init__.py`
to let the `ORM` know it's there and it should be created in the databasen. 


