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


def create_tables():
    sql_users = """ 
          CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY,
            user_parameters jsonb NOT NULL
          )
          """
    sql_items = """ 
          CREATE TABLE IF NOT EXISTS items (
            item_id INT PRIMARY KEY,
            item_parameters jsonb NOT NULL
          )
          """
    c, cur = connect_to_database()
    cur.execute(sql_users)
    cur.execute(sql_items)
    close_database(c, cur)


def insert_data(data, table_name):
    if table_name == 'users':
        id = 'user_id'
        parameters = 'user_parameters'
    elif table_name == 'items':
        id = 'item_id'
        parameters = 'item_parameters'
    else:
        raise Exception('Table name must be users or items')
    sql = """
        INSERT INTO {table_name} VALUES ({id}, '{json_data}')
        ON CONFLICT ({table_id}) DO UPDATE
        SET {parameters} = '{json_data}';
        """
    c, cur = connect_to_database()
    for d in data:
        d.update({'table_name': table_name, 'table_id': id, 'parameters': parameters})
        cur.execute(sql.format(**d))
    logging.info('Successfully inserted or updated {number_entries} entries into Postgres'
                 .format(**{'number_entries': len(data)}))
    close_database(c, cur)


def get_postgres_data(table_name):
    sql = """select * from {table_name}"""
    c, cur = connect_to_database()
    cur.execute(sql.format(**{'table_name': table_name}))
    data = cur.fetchall()
    close_database(c, cur)
    return [{'id': d[0], 'json_data': d[1]} for d in data]
