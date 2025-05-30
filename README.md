# pier2imports
## A Sample Fast API + Postgres Application

### Notes
The app is a simple demo application built on top of fastapi and SQLAlchemy 
with a postgres database.

#### Code Generation
Since I was new to using fast api and SQLAlchemy I decided make it an exercise in 
trying code generation a bit more than usual. I asked ChatGPT 
to guide me through some of the basics of schema creation and best practices 
providing some of the project business requirements.

I then reviewed the schema and made sure that the content made sense. 

For example, a lot of the foreign constraints generated were 
'ON DELETE CASCADE', which I would like to avoid and replaced them 
with RESTRICT instead to prevent deletion of the parent. 
In a real life project, I would likely not always delete the original parent 
row but instead mark the parent data as ‘deleted’ and anonymize it 
if the business rules required so as it is likely we would want to still 
be able to keep the data at least for analytics.

Other little changes where to use auto generated UUIDs as ids instead 
of auto generated integers as I find it to be a better practice.

I continued reviewing the schema to make sure I would be able 
to run the queries required by the api endpoints and adapted the queries
where it was needed.

Once I was happy with the SQL schema, I re-asked Chat GPT to
- regenerate the SQLAlchemy models based on the final SQL Schema
- generate some test data inspired by the Hitchhiker Guide to the Galaxy characters
- generate some unit tests for the ORM models

#### Migrations
The project comes with two SQL scripts that will initialize the database schema and 
populate the database with some minimal data to help testing the app.

These are run as database migrations everytime the application starts.

Because it usually works better for larger projects, I prefer to
rely on migration tools to apply an SQL schema rather than rely on the ORM
to create the schema. The main reason is to be able to control when the
schema is migrated, this is important for example for rolling upgrades
so we can make sure that the schema is migrated and does not break
existing running applications prior to deploying a new version of the
app.

Because of the lack of time, I decided to rely on a simpler tool: [pyway](https://pypi.org/project/pyway/)

At first, I wanted to make it run in the docker file, but it proved to be impractical,
so I decided instead to run it directly from within the python app before 
starting fastapi.

With more time, I would instead use a different tool that integrates better, 
such as alembic of flyway.

As a result of this, I had to do a bit of a hack to run the integration tests.
They rely on having a postgresql database running.
This is a problem because, it will likely make the test fail when the data 
in the database is changed.
With more time, I would instead rely on injecting an in memory database such as
H2 into the integration tests, but making this works properly is beyond the 
scope of this exercise.

### Install and run

#### Clone the repo
From a test directory type:
```
git clone git@github.com:dserfaty/pier2imports.git
```

#### Test with Docker
From the directory where you issued the git clone command type:
```
cd pier2imports
```

And start docker-compose: 
```
docker-compose up
```

This should spawn a docker container for the postgresql database 
and a container for the api application.

Then open a browser to: http://localhost:8000/docs for access to the swagger UI 
and the ability to test the api endpoints.

Later on when you are done testing the application, you can enter the following
to get rid on the containers:
```
docker-compose down
```


#### Sample API Calls

Sample CURL commands for the required api use cases:
```
curl "http://localhost:8000/orders?customer_contact=555-0101"
```
```
curl "http://localhost:8000/orders?customer_contact=arthur.dent%40galaxy.com"
```
```
curl "http://localhost:8000/orders/stats/counts/by_billing_zip?ascending=false&limit=5"
```
```
curl "http://localhost:8000/orders/stats/counts/by_shipping_zip?ascending=false&limit=5"
```
```
curl "http://localhost:8000/orders/stats/in_store_purchases/by_hour?ascending=true"
```
```
curl "http://localhost:8000/orders/stats/top_in_store_users?limit=5"
```

#### Run Locally

If you want to run the application locally or if you wish to run the unit tests.

**Database**

Make sure you have a postgres server (v17) running with 
the following:
```
- an existing database named: pier2imports
- user name: postgres
- password: changemeinprod!
- port: 5432
```

**Create a Virtual Environment and install the requirements**

Make sure to clone the github repository first as described above 
and enter the following commands:

```
cd pier2imports
```
Create a virtual environment:
```
python3 -m venv env
```
And activate it:
```
source env/bin/activate
```
Then install the dependencies:
```
pip install -r requirements.txt
``` 

**Run the App**

Enter the following commands:
```
export DATABASE_HOST=localhost
export DATABASE_NAME=pier2imports
export DATABASE_PASSWORD=changemeinprod!
export DATABASE_PORT=5432
export DATABASE_USER=postgres
export PYWAY_DATABASE_MIGRATION_DIR=migrations

python -m uvicorn app.main:app 
```

#### Run the test cases

With the local postgres database running, Enter the following commands:
```
cd pier2imports
pytest
```
