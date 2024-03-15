import unittest
from main import take_info_about_film


class TakingTest(unittest.TestCase):
    def test_get_error_when_take_info(self):
        with self.assertRaises(TypeError):
            take_info_about_film("l;")


if __name__ == '__main__':
    unittest.main()
