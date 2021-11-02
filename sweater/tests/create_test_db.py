import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

connection = psycopg2.connect(os.environ['TEST_DATABASE_URL'])
# connection = psycopg2.connect('postgresql://postgres:1234@localhost:5432/test_2fa')

connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()


query = f'''CREATE TABLE users(
        id SERIAL PRIMARY KEY,
        login character varying(128),
        password character varying(255),
        pass_img character varying(255),
        counter integer,
        coordinates character varying(128),
        banned integer,
        false_click_counter integer,
        zone character varying(512),
        probability character varying(512)
    )'''
cursor.execute(query)
connection.commit()