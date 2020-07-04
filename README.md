![Deploy to Amazon ECS](https://github.com/Alcasser/tweet-reminder/workflows/Deploy%20to%20Amazon%20ECS/badge.svg?branch=master)

# tweet-reminder
Tweet reminder Twitter bot using Activity and Tweet APIs. Deployed on AWS.

# Local development
Using docker-compose for local development (Nginx, Flask, PostgreSQL)

## Starting services

`docker-compose -f docker-compose.yml -f docker-compose.local.yml build`
`docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d`

This will automatically launch the gunicorn server with the flask api (code changes auto reload) and set up the database.
You can access the api at `localhost:8000`
