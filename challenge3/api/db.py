import psycopg2
import os
from models import create_table
from psycopg2.extras import RealDictCursor

class Database():
    '''constructor to set up database'''
    def __init__(self):
        self.database = os.getenv('DATABASE')
        self.user = os.getenv('USER')
        self.password = os.getenv('PASSWORD') 
        self.host = os.getenv('HOST')
        self.connection = psycopg2.connect(database=self.database, user=self.user,
        	                               host=self.host,password=self.password)


    def create_tables(self):
        cur = self.connection.cursor()
        for table in create_table(self):
            cur.execute(table)
            self.connection.commit()
            print('table created  successfully')
            
        return 'tables created'
      

    def drop_tables(self):
        ''' deletes the existing tables from the database'''
        query = (
        	'DROP TABLE IF EXISTS users CASCADE;',
            'DROP TABLE IF EXISTS questions CASCADE;',
            'DROP TABLE IF EXISTS answers CASCADE;',
            'DROP TABLE IF EXISTS tokens;'
        )
        
        cur = self.connection.cursor()
        for drop_table in query:
            cur.execute(drop_table)
            print('table dropped')
            self.commit()
        
            
        return 'tables dropped successfully'

    def cursor(self):
        '''cursor method for executing queries'''
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        return cur
    
    def commit(self):
        '''save changes to db'''
        self.connection.commit()