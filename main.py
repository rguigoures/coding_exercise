from utils.data_utils import get_random_data
from utils.postgres_utils import create_table, insert_data, get_postgres_data, truncate_postgres
from utils.redis_utils import start_redis, write_batch_into_redis, flush_redis
from multiprocessing import Process
import time
import random


def main_postgres():
    user_data = get_random_data(n=1000)
    create_table()
    truncate_postgres()
    insert_data(user_data)
    while True:
        if random.random() < 0.2:
            number_users_to_update = random.randint(1,100)
            user_data = get_random_data(n=number_users_to_update)
            insert_data(user_data)
        time.sleep(1)


def main_redis():
    r = start_redis()
    flush_redis(r)
    while True:
        time.sleep(5)
        data = get_postgres_data()
        write_batch_into_redis(r, data)


if __name__ == '__main__':
    process_list = []
    for func in [main_postgres, main_redis]:
        p = Process(target=func)
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()

