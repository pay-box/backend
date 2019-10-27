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

## Usage

### Run with docker (Recommended)
You can pull [docker image from docker hub](https://hub.docker.com/r/thesinner/open-pay) and run it with `docker-compose` like this:

```
$ cd docker
$ export PUBLISHED_PORT=6000
$ docker-compose run -d api
```

### Run as a Django project
You can pull [Django standalone repo](https://github.com/theSinner/open-pay) and run it with as a django. Read more in [this repo](https://github.com/theSinner/open-pay).



## Contribution
Any idea is very welcomed and feel free to contribute your or other's ideas.
To submit ideas, please submit an issue with `idea` and if its an improvment, tag it with `improvment` or if its a bug, tag it with `bug`.
if you have fixed an issue, please send a PR and I merge it if its possible.