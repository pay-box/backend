# Open pay


[![DockerHub](https://img.shields.io/docker/pulls/thesinner/open-pay.svg)](https://hub.docker.com/r/thesinner/open-pay) [![Travis](https://travis-ci.org/theSinner/open-pay.svg?branch=master)](https://travis-ci.org/theSinner/open-pay#) ![Commit](https://img.shields.io/github/last-commit/theSinner/open-pay)

Open pay is a service for handling payments with multiple gateways.
Currently supported gateways are:

- [x] Bahamta
- [ ] Zarin pal
- [ ] Sep (Saman Bank)
- [ ] AP (Asan Pardakht)
- [ ] Eghtesad Novin
- [ ] Paypal

## Dependencies
You need `Postgres` and `Redis` to using open pay. You can install them from these links:

* [Postgres](https://www.postgresql.org/docs/12/install-procedure.html)
* [Redis](https://redis.io/topics/quickstart)

## Usage

You can run it with docker using this [image](https://hub.docker.com/r/thesinner/open-pay) or this [repo](https://github.com/theSinner/open-pay-docker).

Anyway if you want to run it as a Django project, you can run it like this:

### Installing python-pip
You can install python pip based on your OS with this [instruction](https://pip.pypa.io/en/stable/installing/)

### Installing virtualenv
```
$ pip install virtualenv
```

### Create a virtualenv
```
$ virtualenv -ppython3 venv
```

### Install dependencies
```
$ source venv/bin/activate
$ pip install -r requirements.pip
```

### Set envrionment variables
There are some envrionment variable to configure:

|Name|Description|Defalut|
|--|--|--|
|BASE_URL|the base url that using in generate websites  |-|
|DEBUG_VALUE|Set debug mode. set TRUE or FALSE|FALSE|
|REDIS_HOST|Redis host|redis|
|REDIS_PORT|Redis port|6379|
|DB_HOST|Postgres database host|db|
|DB_PORT|Postgres database port|5432|
|DB_NAME|Postgres database name|pay|
|MEDIA_ROOT|media folder in project root|media|
|STATIC_ROOT|static folder in project root|static|


### Run project

#### Debug mode
```
$ python manage.py runserver
```
#### Release mode
```
$ uwsgi --http :8100 --wsgi-file pay/wsgi.py --master --processes 6 --threads 2
```



## Contribution
Any idea is very welcomed and feel free to contribute your or other's ideas.
To submit ideas, please submit an issue with `idea` and if its an improvement, tag it with `improvement` or if its a bug, tag it with `bug`.
if you have fixed an issue, please send a PR and I merge it if it's possible.