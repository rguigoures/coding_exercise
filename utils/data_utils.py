import numpy as np
import json
import random


def get_random_data(n=1000):
    data = []
    for i in range(n):
        max_user_number = 10**4
        user_id = random.randint(1, max_user_number)
        json_data = {'latent_vector': np.random.random(10).tolist()}
        data.append({'id': user_id, 'json_data': json.dumps(json_data)})
    return data

