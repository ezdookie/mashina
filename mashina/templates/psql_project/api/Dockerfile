FROM python:3.7.3-alpine3.9
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add supervisor
RUN pip install --upgrade pip

WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt
# RUN pip install https://github.com/ezdookie/mashina/archive/1.0a5.tar.gz
RUN pip install -r ./requirements.txt

COPY . .
RUN pip install -e .

CMD gunicorn --reload {{ project_name }}.wsgi --bind :9066
