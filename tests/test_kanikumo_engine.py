import unittest

import kanikumo_engine


class Kanikumo_engineTestCase(unittest.TestCase):

    def setUp(self):
        self.app = kanikumo_engine.app.test_client()

    def test_index(self):
        rv = self.app.get('/')


if __name__ == '__main__':
    unittest.main()
