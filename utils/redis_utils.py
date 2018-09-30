import redis
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def start_redis():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    return r


def write_batch_into_redis(r, data, feature_name):
    for d in data:
        id = d['id']
        value = d['json_data']
        write_into_redis(r, feature_name, id, value)
    logging.info('Successfully inserted or updated {number_entries} keys into Redis'
                 .format(**{'number_entries': len(data)}))


def write_into_redis(r, feature_name, id, value):
    key = feature_name+'_'+str(id)
    r.set(key, value)
