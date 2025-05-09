import logging
import psycopg2
from configparser import ConfigParser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import errors

def config(filename='database.ini',section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db ={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section,filename))
    return db
def create_db_if_not_exits():
    params = config()
    db_name =  params['database']

    admin_params =  params.copy()
    admin_params['database'] ='postgres'
    try:
        conn =  psycopg2.connect(**admin_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        try:
            cur.execute(f'CREATE DATABASE"{db_name}"')
            print(f"database{db_name} successfully created .")
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database '{db_name}' already exits")
        finally:
            cur.close()
            conn.close()
    except Exception as e :
        print(f" Could not sure DB exists : {e}")
