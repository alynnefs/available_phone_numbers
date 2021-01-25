# Available phone numbers

This project manages [DID Numbers](https://www.3cx.com/pbx/did/) in inventory.

Clicking the button below you can see some examples of how the API works.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/3d77d377005a688d1e11)

## Used setup
This project was coded and tested in `Ubuntu 18.04`, `Docker version 20.10.2`, `docker-compose version 1.27.4` and `Python 3.6.9`.

## How to run with docker

```
docker-compose up
```

## How to run outside the docker image


create a virtual enviroment
```
virtualenv --python=/usr/bin/python3.6 .venv
source .venv/bin/activate
```
run the API
```
python application/app/api.py
```

run the tests
```
python application/app/unit_tests.py
```


