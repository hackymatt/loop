FROM python:3.9-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy main.sh
COPY ./main.sh .
RUN sed -i 's/\r$//g' /usr/src/app/main.sh
RUN chmod +x /usr/src/app/main.sh

# copy project
COPY . .

# run main.sh
ENTRYPOINT ["/usr/src/app/main.sh"]