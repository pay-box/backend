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

## Run

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

## How to use it
There are few ways to handle payments. The entities are:

### Application
Applications are for set tokens for using web APIs.

### Gateway
Gateways are methods that provide payments. Currently we support only [Bahamta](https://bahamta.com) type gateways. You can add gateways to use them to pay.

### Form
Forms are for making templates to generate payments. You can have a fixed or dyanmic amount that users enter it before pay or you can set one or more gateways to be available for users.

### Transaction
Transactions are payment logs. Pending payments are stored in Redis, but successful or rejected payments store in database.


### Create Request
You can make request with api.
```
curl -X POST \
  https://openpay.ajorloo.com/api/transaction/make \
  -H 'Access-Token: YOUR_APPLICATION_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
	"amount": 10000,
	"currency": "irr",
	"gateway_id": 1,
    "continue_url": "https://google.com",
    "phone_number": "989xxxxxxxxx",
    "email" : "amirajorloo@gmail.com",
    "username" : "fdsfsewrwer423423o4iewor3",
  }'
```

The `currency` parameter is required and others are optional parameters. If you send `amount`, the amount is fixed and if amount is empty, amount is dyanmic and user will enter it and if you send `gateway_id`, the payment transaction will be fixed and if not, user should choose from gateways with entered `currency`. The `continue_url` is the url that show to user when payment is completed. `phone_number`, `email`, and `username` are fields for set user for transaction. if all of them is empty or username doesn't exist in user database, create new user and set transaction to it.

### Get Transaction Detail
You can get transaction detail with this endpoint.
```
curl -X GET \
  https://openpay.ajorloo.com/api/transaction/item?ref_num=xxXXxxXXxx \
  -H 'Access-Token: YOUR_APPLICATION_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache'
```
  

## Contribution
Any idea is very welcomed and feel free to contribute your or other's ideas.
To submit ideas, please submit an issue with `idea` and if its an improvement, tag it with `improvement` or if its a bug, tag it with `bug`.
if you have fixed an issue, please send a PR and I merge it if it's possible.