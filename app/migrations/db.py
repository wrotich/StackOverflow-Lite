import psycopg2
import psycopg2.extras
import os
from .sql_setup import migrations
from config import BaseConfig
from ..helpers import db_config


class Database:
    def __init__(self):
        self.config = db_config()
        self.database = self.config.get('database')

    def migrate(self):
        con = psycopg2.connect(**self.config)
        con.autocommit = True
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("select * from pg_database where datname = %(database_name)s", {'database_name': self.database})
        databases = cur.fetchall()
        if len(databases) > 0:
            print(" * Database {} exists".format(self.database))
            for command in migrations:
                cur.execute(command)
                con.commit()
        else:
            print(" * Database {} does not exists".format(self.database))
        con.close()

    def migrate_test_db(self):
        """ Create test database and schema """
        os.environ['APP_SETTINGS'] = 'TESTING'
        con = psycopg2.connect(**self.config)
        con.autocommit = True
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('CREATE DATABASE {} OWNER {};'.format(BaseConfig.TEST_DB, self.config.get('user')))
        con.close()
        self.config['database'] = BaseConfig.TEST_DB
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        for command in migrations:
            cur.execute(command)
            con.commit()
        con.close()

    def drop_test_database(self):
        self.config = db_config()
        con = psycopg2.connect(**self.config)
        con.autocommit = True
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('DROP DATABASE IF EXISTS {};'.format(BaseConfig.TEST_DB, self.config.get('user')))
        con.close()


db = Database()
