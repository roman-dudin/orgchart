import unittest

from cli_client import chart_client
from cli_client.chart_client import WrongInputException


class ParseInput(unittest.TestCase):

    def test_parse_input_without_quotes(self):
        with self.assertRaises(WrongInputException):
            chart_client.parse_input('B1,E1,E2,E3')

    def test_parse_input_for_1_string(self):
        result = chart_client.parse_input('"B1,E1,E2,E3"')
        self.assertEqual('[["B1", "E1", "E2", "E3"]]', result)

    def test_parse_input_for_3_strings(self):
        result = chart_client.parse_input('"B1,E1,E2,E3" "B2,E21,E22" "B3,E31"')
        self.assertEqual('[["B1", "E1", "E2", "E3"], ["B2", "E21", "E22"], ["B3", "E31"]]', result)
