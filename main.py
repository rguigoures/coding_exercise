from utils.data_utils import get_random_data
from utils.postgres_utils import create_tables, insert_data, get_postgres_data
from utils.redis_utils import start_redis, write_batch_into_redis
from multiprocessing import Process
import time
import random


def main_postgres():
    user_data = get_random_data(n=1000)
    item_data = get_random_data(n=100)
    create_tables()
    insert_data(user_data, 'users')
    insert_data(item_data, 'items')
    while True:
        time.sleep(1)
        if random.random() < 0.2:
            user_data = get_random_data(n=100)
            item_data = get_random_data(n=10)
            create_tables()
            insert_data(user_data, 'users')
            insert_data(item_data, 'items')


def main_redis():
    r = start_redis()
    while True:
        for feature_name in ['users', 'items']:
            data = get_postgres_data(feature_name)
            write_batch_into_redis(r, data, feature_name)
        time.sleep(5)


if __name__ == '__main__':
    process_list = []
    for func in [main_postgres, main_redis]:
        p = Process(target=func)
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()

