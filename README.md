# Job Hunt
This repository provides API endpoints for a job-seeker (job_hunter) to view jobs and apply for the job of interest. 
It is built on Django and Django Rest Framework.

You can set up the project both without and with Docker. Firstly, we will set up the project without Docker, and then 
with Docker.

## Without Docker
### Clone Repository
The first step is to clone the repository, to do that, run the following command:
```shell
git clone https://github.com/KhawajaAhmad/job_hunt.git
```

### Virtual Environment
Now, create a virtual environment and activate it.
```shell
python -m venv env
source env/bin/activate
```

### Install Dependencies
To install dependencies, run the following command:
```
pip install -r requirements.txt
```

## With Docker
1. Install Docker
2. To build the image and run the app, execute the following commands respectively:
```shell
sudo docker build . -t job_hunt
sudo docker run job_hunt
```

## Migrations
After setting up the project, run the following command to migrate database changes:
```shell
python manage.py migrate
```

## Run
To run the server, run the following command:
```shell
python manage.py runserver
```
