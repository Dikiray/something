#!/bin/bash
set -e

python3 prepare.py
exec gunicorn main:app --bind 0.0.0.0:80 -w ${gunicorn_workers_count:-4}
