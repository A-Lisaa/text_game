import unittest

from src.storage import Storage


class StorageTest(unittest.TestCase):
    def test_creation(self):
        storage = Storage(cells_threshold=10)
        self.assertEqual(str(storage), str([[] for _ in range(10)]))
