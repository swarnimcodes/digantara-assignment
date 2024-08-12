# digantara-assignment

This is a python based microservice developed as part of an assignment for Digantara.
The objective is to develop a job scheduling microservice which is scalable and modular.

## Features

The backend has the following features:
- **Job Scheduling**: Schedule jobs without having to learn a new way of scheduling things. Just use the cron syntax.
  This removes the need to maintain code for custom scheduling and instead relies on tried and tested cron jobs
  making scheduling as customizable as you want. The system uses the IST timezone for convenient scheduling.
- **Database Integration**: The backend uses the robust, quick and reliable SQLite database. SQLite is well tested
  for over 2 decades. The backend also uses SQLAlchemy as the ORM which would make shifting to a different database
  a breeze. SQLite will also scale very well and if the scale management becomes tedious, we could hand over the
  scaling department to Turso and forget about database bottlenecks while maintaining SQLite as the database.
- **Schedule Customization**: Since we use cron jobs, sky is the limit for custom scheduling.
- **API Documentation**: Creating and maintaining an up-to-date API Documentation manually is an endless pursuit.
  Documentation can quickly become old and irrelevant if not catered to.
  But code will never be "out of date".
  Hence, the choice of our API Framework, i.e. [FastAPI](https://fastapi.tiangolo.com/) really shines here 
  with the built-in API documentation that is generated from code itself. 
  We can even test the API from within the documentation and remove reliance
  upon services such as [Postman](https://www.postman.com/) and [HTTPie](https://httpie.io/) (albeit they are still indespensible).

## Setup

**0. Get the dependencies**

```sh
$ sudo pacman -Syu python git uv --needed
```
  This backend was tested to work on arch linux using python version 3.12.4

**1. Clone the repository**

```sh
$ git clone "https://github.com/swarnimcodes/digantara-assignment.git" && cd digantara-assignment
```

**2. Create and activate virtual environment**

```sh
$ uv venv && source .venv/bin/activate
```
Why uv? ==> https://astral.sh/blog/uv

This guide will work with the default way of creating virtual environments using `python -m venv .venv`
as well. Source the envireonment to activate it before moving ahead.
Using uv seems like a better choice from what I understand.

**3. Install the project requirements**

```sh
$ uv pip install -r requirements.txt
```

OR if not using uv then:

```sh
$ pip install -r requirements.txt
```

**4. Run the Backend API:**

```sh
$ python -m uvicorn scheduler:app --reload
```

That's it. The backend should be up and running on port 8000 while also watching for any changes in the project files.

**5. Documentation:**

Since we are using the brilliant FastAPI web framework, the API documentation is auto-generated through our code and is
testable from within the documentation.
Head over to `http://localhost:8000/docs` and you will be presented with the up-to-date API documentation.
This page also allows us to quickly get our OpenAPI Spec for the API we have built! Super handy.

## API Endpoints

The API has the following endpoints:

1. `GET /jobs`
  This lists all the jobs that we have ever created and that are stored within our database.
  I have also built in simple pagination for a little futureproofing.
  A simple get request should work.
2. `GET /jobs/:id`
  Fetch details regarding a specific job with a given job id.
3. `POST /jobs`
  Create a new job with custom scheduling capabilities.
  Input needs to be a JSON Body of the following form:
    ```json
    {
      "cron_string": "string"
    }
    ```
  You may use https://crontab.guru/ for a simple and intuitive cron syntax helper.
  Another wonderful piece of documentation is the manpage for crontab.
  If on a linux machine, type in `man 5 crontab` to bring up the documentation
  that talks about scheduling syntax. 5 here obviously represents the "conventions" section
  of the linux manual.
  You could also visit the online hosted documentation for crontab here: https://www.man7.org/linux/man-pages/man5/crontab.5.html
   
