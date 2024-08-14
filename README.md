# Django Payment Project

This project is a payment system implemented using the Django framework. It features a custom user model with fields `username` and `telegram_id`, as well as CRUD operations for transactions and balances. It also includes an API endpoint for summarizing transaction data.

## Installing using GitHub

Install PostgresSQL and create db

```shell
git clone https://github.com/tiron-vadym/django-payment-project
cd payment_API
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db username>
set DB_PASSWORD=<your db user password>
set SECRET_KEY=<your secret key>
python manage.py migrate
python manage.py runserver
```

## Run with docker

Docker should be installed

```shell
docker-compose --build
docker-compose up
```

## Getting access(JWT authenticated)

* Create user via /client/register
* Get access token via /client/token

## Endpoints

- Admin Panel: `/admin/`
- Service API: `/payment/`
- Client API: `/client/`

## Features

  - CRUD operations for `balances` and `transactions`.
  - Logout functionality `/logout/` for users in JWT.
  - Endpoint `/payment/transaction/summary/` to get summary data for transactions over the past few days.

## Debugging and Documentation

- Debug Toolbar: `/__debug__/`
- API Schema: `/api/schema/`
- Swagger Documentation: `/api/swagger/`
