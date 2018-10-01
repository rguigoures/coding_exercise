from utils.data_utils import get_random_data
from utils.postgres_utils import create_table, insert_data, truncate_postgres
from utils.redis_utils import start_redis, flush_redis


def main_redis():
    r = start_redis()
    flush_redis(r)


def main_postgres():
    create_table()
    truncate_postgres()
    user_data = get_random_data(n=100000)
    insert_data(user_data)


if __name__ == '__main__':
    main_postgres()
    main_redis()