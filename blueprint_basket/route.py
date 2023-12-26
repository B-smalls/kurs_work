import os

from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_context_manager import DBContextManager
from db_work import select_dict, select, insert, update
from sql_provider import SQLProvider
from datetime import date
from access import group_required, login_required
import re

blueprint_order = Blueprint('bp_order', __name__, template_folder='templates', static_folder='static')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order.route("/")
@login_required
@group_required
def order_list():
    return render_template('select_menu_order.html')


@blueprint_order.route('/search_flight', methods=['GET', 'POST'])
@login_required
@group_required
def search_flight():
    if request.method == 'GET':
        sql = provider.get('all_city_dep.sql')
        c_dep = select_dict(current_app.config['db_config'], sql)

        sql = provider.get('all_airport_dep.sql')
        a_dep = select_dict(current_app.config['db_config'], sql)

        sql = provider.get('all_city_ariv.sql')
        c_ariv = select_dict(current_app.config['db_config'], sql)

        sql = provider.get('all_airport_ariv.sql')
        a_ariv = select_dict(current_app.config['db_config'], sql)

        return render_template('start_basket_order_list.html', c_dep=c_dep, a_dep=a_dep, c_ariv=c_ariv, a_ariv=a_ariv)
    else:
        dep_city = request.form.get('dep_city')
        name_airport_dep = request.form.get('name_airport_dep')
        ariv_city = request.form.get('ariv_city')
        name_airport_ariv = request.form.get('name_airport_ariv')
        dep_date_time = request.form.get('dep_date_time')
        if dep_city and name_airport_dep and ariv_city and name_airport_ariv and dep_date_time:
            sql = provider.get('search_flight.sql', dep_city=dep_city, ariv_city=ariv_city,
                                name_airport_dep=name_airport_dep, name_airport_ariv=name_airport_ariv,
                                dep_date_time=dep_date_time)

            tickets = select_dict(current_app.config['db_config'], sql)
            print("ticket=", tickets)
            if tickets:
                session['tickets'] = tickets
                return redirect(url_for('bp_order.order_index'))
            else:
                return render_template('error_not_found.html')
        else:
            return redirect(url_for('bp_order.search_flight'))


@blueprint_order.route('/choise_ticket', methods=['GET', 'POST'])
@login_required
@group_required
def order_index():
    if request.method == 'GET':
        items = session.get('tickets')
        return render_template('basket_order_list.html', items=items)
    else:
        session['t_id'] = request.form['t_id']
        session.permanent = True
        return redirect(url_for('bp_order.input_data'))


@blueprint_order.route('/input_data', methods=['GET', 'POST'])
@login_required
@group_required
def input_data():
    if request.method == 'GET':
        t_id = session.get('t_id')
        print(t_id)
        return render_template('input_data.html')
    else:
        FullName = request.form.get('FullName')
        passport_data = request.form.get('passport_data')
        if FullName and passport_data:
            if check_input_data(FullName, passport_data):
                FullName = format_name(FullName)
                print(FullName)
                t_id = session.get('t_id')
                user_id = session.get('user_id')
                order_id = save_order_with_list(current_app.config['db_config'], user_id, t_id, FullName, passport_data)
                if order_id:
                    session.pop('tickets')
                    session.pop('t_id')
                    return render_template('order_created.html', order_id=order_id)
                else:
                   return render_template('order_error.html')
            else:
                return render_template('input_data.html', error_message="Вы ввели некорректные данные. Повторите ввод.")
        else:
            return render_template('input_data.html', error_message="Вы не ввели данные. Повторите ввод.")

@blueprint_order.route('/view_buy_ticket')
@login_required
@group_required
def view_buy_ticket():
    user_id = session.get('user_id')
    _sql = provider.get('view.sql', user_id=user_id)
    result, schema = select(current_app.config['db_config'], _sql)
    list_name = ['Номер заказа', 'Дата покупки', 'Город вылета', 'Аэропорт вылета', 'Город прилета',
                 'Аэропорт прилета', 'Дата и время вылета', 'Дата и время прилета', 'Место в самолете', 'Цена']
    return render_template('view_buy.html', schema=list_name, result=result)



def save_order_with_list(dbconfig: dict, user_id: int, t_id: int, FullName: str, passport_data: str):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        _sql1 = provider.get('insert_order.sql', user_id=user_id, order_date=date.today())
        print(_sql1)
        result1 = insert(current_app.config['db_config'], _sql1)
        if result1 == 1:
            _sql4 = provider.get('update_ticket.sql', FullName=FullName, passport_data=passport_data, t_id=t_id, order_date=date.today())
            print(_sql4)
            result2 = update(current_app.config['db_config'], _sql4)
            if result2 == 1:
                _sql2 = provider.get('select_order_id.sql', user_id=user_id)
                cursor.execute(_sql2)
                order_id = cursor.fetchall()[0][0]
                print('order_id=', order_id)
                if order_id:
                    _sql3 = provider.get('insert_order_list.sql', order_id=order_id, t_id=t_id)
                    insert(current_app.config['db_config'], _sql3)
                    return order_id

def check_input_data(FullName: str, passport_data: str) -> bool:
    result_1 = re.compile(r'^[А-Яа-я]+ [А-Яа-я]+( [А-Яа-я]+)?$')
    result_2 = re.compile(r'^\d{4} \d{6}$')
    if re.search(result_1, FullName) and re.search(result_2, passport_data):
        return True
    else:
        return False

def format_name(FullName: str):
    format_name=FullName.split(" ")
    correct_name=""
    for name in format_name:
        correct_name = correct_name + name.capitalize()+" "
    return correct_name


