#!/usr/bin/env bash

source .venv/bin/activate
mkdir backups
python manage.py dumpdata billing>backups/billing.json
python manage.py dumpdata business>backups/business.json
python manage.py dumpdata comment>backups/comment.json
python manage.py dumpdata currency>backups/currency.json
python manage.py dumpdata lead>backups/lead.json
python manage.py dumpdata location>backups/location.json
python manage.py dumpdata order>backups/order.json
python manage.py dumpdata outlet>backups/outlet.json
python manage.py dumpdata product>backups/product.json
python manage.py dumpdata taxation>backups/taxation.json
python manage.py dumpdata drf_user>backups/users.json
python manage.py dumpdata drf_paytm>backups/paytm.json
python manage.py dumpdata drf_instamojo>backups/instamojo.json
