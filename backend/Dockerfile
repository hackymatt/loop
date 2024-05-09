FROM python:3.9-slim

# set work directory
WORKDIR /usr/src/app/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install postgresql-client-15 cron libpq-dev gcc \
    && pip install psycopg2

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

EXPOSE 8000

# run main.sh
RUN ["chmod", "+x",  "./main.sh"]
ENTRYPOINT ["./main.sh"]