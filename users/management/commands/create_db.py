
import os

from django.core.management.base import BaseCommand

import psycopg2
from decouple import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Only run if Debug=True (so it's not run in production environments, as this is only useful for dev)
if config('DEBUG'):
    DB_NAME = config('DB_NAME')
    DB_USER = config('DB_USER')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_HOST = config('DB_HOST')


class Command(BaseCommand):
    '''Custom command to create a psql database'''

    def handle(self, *args, **kwargs):
        print('Creating database...')
        self._create()

    def _create(self):
        conn = psycopg2.connect(user="postgres",
                                host='localhost')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # To CREATE DB from python

        cur = conn.cursor()
        cur.execute(f'DROP DATABASE IF EXISTS {DB_NAME};')
        cur.execute(f'CREATE DATABASE {DB_NAME};')
        cur.execute(f'DROP USER IF EXISTS {DB_USER};')
        cur.execute(f"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';")
        cur.execute(f"ALTER ROLE {DB_USER} SET client_encoding TO 'utf8';")
        cur.execute(f"ALTER ROLE {DB_USER} SET default_transaction_isolation TO 'read committed';")
        cur.execute(f"ALTER ROLE {DB_USER} SET timezone TO 'UTC';")
        cur.execute(f'GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};')
        cur.execute(f'ALTER USER {DB_USER} CREATEDB;')
        conn.commit()
        conn.close()

