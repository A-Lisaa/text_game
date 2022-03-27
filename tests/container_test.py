import unittest

from src.utils.container import Container


class ContainerTest(unittest.TestCase):
    def test_get_default_item(self):
        container = Container(default_value=[0, 1, 2])
        self.assertEqual(container["test"], [0, 1, 2])

    def test_set_by_equals(self):
        container = Container()
        container["test"] = 1488
        self.assertEqual(container["test"], 1488)

    def test_set_by_plus_equals(self):
        container = Container()
        container["test"] = 1488
        container["test"] += 666
        self.assertEqual(container["test"], 2154)

    def test_set_to_zero(self):
        container = Container()
        container["test"] = 666
        self.assertEqual(container["test"], 666)
        container["test"] -= 666
        self.assertEqual(container["test"], 0)


if __name__ == "__main__":
    unittest.main()
