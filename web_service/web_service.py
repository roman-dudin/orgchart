from flask import Flask, render_template, url_for, request, redirect
import json

app = Flask(__name__)

path_to_chart_file = '../chart'


def chart_from_file_data():
    with open(path_to_chart_file, 'r') as file:
        data = file.readlines()
    c = {}
    for line in data:
        tmp = line.split(',')
        t1 = tmp.pop(0)
        c[t1] = tmp
    return c


@app.route('/')
@app.route('/index')
def route_index():
    chart = chart_from_file_data()
    return render_template('index.html', chart=chart)


@app.route('/api/orgchart/new', methods=['GET', 'POST'])
def route_reset_org_chart():
    reset_org_chart()
    return redirect(url_for('route_index'))


def reset_org_chart():
    open(path_to_chart_file, 'w').close()


@app.route('/api/orgchart/fill_test_data', methods=['GET', 'POST'])
def route_fill_test_data():
    fill_test_data()
    return redirect(url_for('route_index'))


def fill_test_data():
    with open(path_to_chart_file, 'w') as file:
        file.write('B1, E1, E2, E3, E4\nB2, E21, E22\nB3, E31, E32, E33, E34')


@app.route('/api/orgchart/add', methods=['POST'])
def route_add():
    add(json.JSONDecoder().decode(request.data.decode("utf-8")))
    return redirect(url_for('route_index'))


def add(data):
    with open(path_to_chart_file, 'a') as file:
        for node in data:
            file.write('\n')
            file.write(','.join(node))


@app.route('/api/orgchart/<int:_id>', methods=['DELETE'])
def route_drop(_id):
    drop(_id)
    return redirect(url_for('route_index'))


def drop(_id):
    with open(path_to_chart_file, 'r+') as file:
        lines = file.readlines()
        del lines[_id - 1]
        lines[-1] = lines[-1].rstrip()
        file.seek(0)
        file.truncate()
        file.writelines(lines)


if __name__ == '__main__':
    app.run(debug=True)
