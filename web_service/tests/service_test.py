import unittest

from web_service import web_service

path_to_test_chart_file = 'tests_chart'


def fill_test_chart_file_with_sample_data():
    with open(path_to_test_chart_file, 'w') as file:
        file.write('B1, E1, E2, E3, E4\nB2, E21, E22\nB3, E31, E32, E33, E34')


class ServiceTest(unittest.TestCase):

    def setUp(self):
        web_service.path_to_chart_file = path_to_test_chart_file
        fill_test_chart_file_with_sample_data()

    def test_reset_file(self):
        with open(path_to_test_chart_file, 'r') as file:
            lines = file.readlines()
        self.assertEqual(['B1, E1, E2, E3, E4\n', 'B2, E21, E22\n', 'B3, E31, E32, E33, E34'], lines)
        web_service.reset_org_chart()
        with open(path_to_test_chart_file, 'r') as file:
            lines = file.readlines()
        self.assertEqual([], lines)

    def test_add_1_item(self):
        with open(path_to_test_chart_file, 'r') as file:
            lines = file.readlines()
        self.assertNotIn('A,B,C', lines)
        web_service.add([['A', 'B', 'C']])
        with open(path_to_test_chart_file, 'r') as file:
            lines = file.readlines()
        self.assertIn('A,B,C', lines)

    def test_add_2_items(self):
        with open(path_to_test_chart_file, 'r') as file:
            lines = file.readlines()
        self.assertNotIn('A,B,C\n', lines)
        self.assertNotIn('D,E,F', lines)
        web_service.add([['A', 'B', 'C'], ['D', 'E', 'F']])
        with open(path_to_test_chart_file, 'r') as file:
            lines = file.readlines()
        self.assertIn('A,B,C\n', lines)
        self.assertIn('D,E,F', lines)

    def test_drop_first_item(self):
        with open(path_to_test_chart_file, 'r') as file:
            lines = file.readlines()
        self.assertIn('B1, E1, E2, E3, E4\n', lines)
        web_service.drop(1)
        with open(path_to_test_chart_file, 'r') as file:
            lines = file.readlines()
        self.assertNotIn('B1, E1, E2, E3, E4\n', lines)

    def test_drop_middle_item(self):
        with open(path_to_test_chart_file, 'r') as file:
            lines = file.readlines()
        self.assertIn('B2, E21, E22\n', lines)
        web_service.drop(2)
        with open(path_to_test_chart_file, 'r') as file:
            lines = file.readlines()
        self.assertNotIn('B2, E21, E22\n', lines)

    def test_drop_last_item(self):
        with open(path_to_test_chart_file, 'r') as file:
            lines = file.readlines()
        self.assertIn('B3, E31, E32, E33, E34', lines)
        web_service.drop(3)
        with open(path_to_test_chart_file, 'r') as file:
            lines = file.readlines()
        self.assertNotIn('B3, E31, E32, E33, E34', lines)
