import redis
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def start_redis():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    return r


def flush_redis(r):
    r.flushall()


def write_batch_into_redis(r, data):
    for d in data:
        id = d['user_id']
        value = d['user_parameters']
        write_into_redis(r, id, value)
    logging.info('Successfully wrote {number_entries} keys into Redis'
                 .format(**{'number_entries': len(data)}))


def write_into_redis(r, id, value):
    key = id
    r.set(key, value)
