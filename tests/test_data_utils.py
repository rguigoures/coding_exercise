import unittest
from utils.data_utils import get_random_data


class TestDataUtils(unittest.TestCase):
    def test_data_generation(self):
        data = get_random_data(n=10)
        self.assertEqual(len(data), 10)
        for d in data:
            self.assertListEqual(list(d.keys()), ['id', 'json_data'])
            self.assertEqual(type(d['id']), int)
            self.assertEqual(type(d['json_data']), str)


if __name__ == '__main__':
    unittest.main()
