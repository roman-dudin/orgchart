from requests import request
import json
from configparser import ConfigParser

server = ''


def main():
    global server
    config = ConfigParser()
    config.read('../config.ini')
    server = config['server']['server_address']
    print('Please print command. Print cli help to view available commands.')
    while True:
        command = input()
        if command == 'cli help':
            print_help()
            continue
        if command == 'cli reset':
            cli_reset()
            continue
        if command == 'cli filltestdata' or command == 'cli ftd':
            cli_fill_test_data()
            continue
        if command.startswith('cli add '):
            cli_add(command[8:])
            continue
        if command.startswith('cli drop '):
            cli_drop(command[9:])
            continue
        if command == 'exit':
            break
        print('Unknown command "{}"'.format(command))
        print_help()


def print_help():
    print("""Available commands:
             exit
             cli reset - to reset org chart
             cli filltestdata - to fill chart with sample data
             cli add 'data to add' - to add new data to chart """)


def cli_reset():
    request('POST', server + '/api/orgchart/new')
    print('chart has been reseted')


def cli_fill_test_data():
    request('POST', server + '/api/orgchart/fill_test_data')
    print('chart has been filled with test data')


def cli_add(data):
    try:
        parsed_data = parse_input(data)
    except WrongInputException as e:
        print(e.value)
        return
    request('POST', server + '/api/orgchart/add', data=parsed_data)
    print('Added ' + data)


def cli_drop(_id):
    request('DELETE', server + '/api/orgchart/' + _id)
    print('Deleted')


# "B1,E1,E2,E3" ["B2,E34,E55,E11" ...]
def parse_input(s):
    if not (s.startswith('"') and s.endswith('"')):
        raise WrongInputException('Wrong input format! Should be "B1,E1,E2,E3" ["B2,E34,E55,E11" ...]')
    s = s[1:-1]
    nodes = s.split('" "')
    result = []
    for node in nodes:
        result.append(node.split(','))
    return json.dumps(result)


class WrongInputException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


if __name__ == '__main__':
    main()
