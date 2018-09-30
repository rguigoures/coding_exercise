import numpy as np
import json


def get_random_data(n=1000):
    data = []
    for i in range(n):
        json_data = {'latent_vector': np.random.random(10).tolist()}
        data.append({'id': i, 'json_data': json.dumps(json_data)})
    return data

