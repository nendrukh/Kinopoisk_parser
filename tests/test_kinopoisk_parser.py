from unittest.mock import patch
from unittest import TestCase
from main import take_info_about_film, ask_user


def get_input(text):
    return input(text)


class ParserTest(TestCase):
    def test_get_error_when_take_info(self):
        with self.assertRaises(TypeError):
            take_info_about_film("l;")

    @patch('test_kinopoisk_parser.get_input', return_value=1)
    def test_user_input_1(self, input):
        self.assertEqual(ask_user(), 1)
