# async oauth
Dockerized async oauth client using aioauth-client

## Usage:
```
Edit the core/conf.py configurations with your own credentials

default url: http://localhost:8000/oauth/{provider}
eg.: http://localhost:8000/oauth/google
```

## Available Providers
Providers: google, facebook, twitter, github, bitbucket, yandex.

## Running:
```
$ docker-compose build 
$ docker-compose up
```
