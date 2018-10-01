import psycopg2
from configs import DBNAME, USERNAME, HOST, PASSWORD
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(process)d %(message)s')


def connect_to_database():
    c = psycopg2.connect(dbname=DBNAME, user=USERNAME, host=HOST, password=PASSWORD)
    cur = c.cursor()
    return c, cur


def close_database(c, cur):
    cur.close()
    c.commit()
    c.close()


def create_table():
    sql_users = """ 
          CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY,
            user_parameters jsonb NOT NULL
          )
          """
    c, cur = connect_to_database()
    cur.execute(sql_users)
    close_database(c, cur)


def truncate_postgres():
    sql = """delete from users"""
    c, cur = connect_to_database()
    cur.execute(sql)
    close_database(c, cur)


def insert_data(data):
    sql = """
        INSERT INTO users VALUES ({id}, '{json_data}')
        ON CONFLICT (user_id) DO UPDATE
        SET user_parameters = '{json_data}';
        """
    c, cur = connect_to_database()
    for d in data:
        cur.execute(sql.format(**d))
    logging.info('Successfully inserted or updated {number_entries} users into Postgres'
                 .format(**{'number_entries': len(data)}))
    close_database(c, cur)


def get_postgres_data(limit, offset):
    sql = """select * from users LIMIT {limit} OFFSET {offset}""".format(**{'limit': limit, 'offset': offset})
    c, cur = connect_to_database()
    cur.execute(sql)
    data = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    close_database(c, cur)
    return [{desc: d[i] for i, desc in enumerate(column_names)} for d in data]
