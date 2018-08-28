
import unittest
from .base import BaseTestCase
from ..migrations.db import Database
from ..migrations.sql_setup import create_tables_commands


class DatabaseTestCase(BaseTestCase):

    def test_database_configuration(self):
        '''Tests for the correct database configs.'''
        db = Database()
        self.assertEqual(len(db.config.keys()), 4)

    def test_database_tables(self):
        self.assertEqual(len(create_tables_commands), 3)


if __name__ == '__main__':
    unittest.main()
