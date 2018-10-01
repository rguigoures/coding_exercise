from utils.postgres_utils import insert_data, get_postgres_data
from utils.redis_utils import start_redis, write_batch_into_redis, flush_redis
from multiprocessing import Process
from configs import NR_PROCESS, BATCH_SIZE
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def update_redis(redis_connector, process_id):
    iteration = 0
    while True:
        data = get_postgres_data(limit=BATCH_SIZE, offset=BATCH_SIZE * (NR_PROCESS * iteration + process_id))
        if data:
            write_batch_into_redis(redis_connector, data)
            iteration += 1
        else:
            return 0


def multithread_redis_update():
    redis_connector = start_redis()
    process_list = []
    for process_id in range(NR_PROCESS):
        p = Process(target=update_redis, args=(redis_connector, process_id))
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()
    logging.info("REDIS SUCCESSFULLY UPDATED")


if __name__ == '__main__':
    r = start_redis()
    flush_redis(r)
    while True:
        time.sleep(5)
        multithread_redis_update()


