version: '2.1'

services:
  common_postgres_db:
    image: postgres:9.6
    environment:
      - PGDATA=/var/lib/postgresql/data/pgdata

  common_api:
    build: ./api
    volumes:
      - ./api/{{ project_name }}:/usr/src/app/{{ project_name }}
      - ./api/tests:/usr/src/app/tests
    ports:
      - "9066:9066"
