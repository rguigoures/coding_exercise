from utils.data_utils import get_random_data
from utils.postgres_utils import insert_data
import random
import time


def randomly_triggered_loading():
    while True:
        if random.random() < 0.2:
            number_users_to_update = random.randint(1,10)
            user_data = get_random_data(n=number_users_to_update)
            insert_data(user_data)
        time.sleep(.1)


if __name__ == '__main__':
    randomly_triggered_loading()