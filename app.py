from flask import Flask, url_for, render_template, json, session, redirect

from blueprint_auth.route import blueprint_auth
from blueprint_query.route import blueprint_query
from blueprint_basket.route import blueprint_order
from blueprint_report.route import blueprint_report

app = Flask(__name__)

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/requests')
app.register_blueprint(blueprint_order, url_prefix='/order')
app.register_blueprint(blueprint_report, url_prefix='/report')

app.config['db_config'] = json.load(open('data_files/dbconfig.json'))
app.config['access_config'] = json.load(open('data_files/access.json'))
app.config['report_url'] = json.load(open('data_files/report_url.json'))
app.config['report_list'] = json.load(open('data_files/report_list.json', encoding='UTF-8'))

app.secret_key = 'Aviasales'


@app.route('/', methods=['GET', 'POST'])
def menu_choice():
    if 'user_id' in session:
        return render_template('index_process.html')
    else:
        return render_template('index_begin.html')

@app.route('/exit')
def exit_func():
    if 'user_id' in session:
        session.pop('user_id')
    if 'user_group' in session:
        session.pop('user_group')
    return redirect(url_for('menu_choice'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
