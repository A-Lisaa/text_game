import os
import unittest

from src.utils.lines import Lines

_lines = Lines(os.path.abspath("./tests/lines_test.json"))

class LinesTest(unittest.TestCase):
    def test_get_line(self):
        self.assertEqual(_lines["test_string"], "String for Test")
        self.assertEqual(_lines["test_int"], 1488)
        self.assertEqual(_lines["test_float"], 666.666)
        self.assertEqual(_lines["test_bool"], True)

    def test_get_wrong_line(self):
        self.assertEqual(_lines["wrong_name"], "wrong_name")
