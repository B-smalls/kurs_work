import os

from flask import Blueprint, request, render_template, current_app
from db_work import select
from sql_provider import SQLProvider
from access import group_required, login_required

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route("/")
@login_required
@group_required
def query_list():
    return render_template('select_menu_new.html')


@blueprint_query.route('/task1', methods=['GET', 'POST'])
@login_required
@group_required
def task1():
    if request.method == 'GET':
        return render_template('flight_number_form.html')
    else:
        input_flight_number = request.form.get('input_flight_number')
        if input_flight_number:
            _sql = provider.get('flight.sql', input_flight_number=input_flight_number)
            flight_number_result, schema = select(current_app.config['db_config'], _sql)
            if not flight_number_result:
                return render_template('flight_number_form.html', error_message="Данных не найдено")
            else:
                list_name=['Номер рейса', 'Город вылета', 'Город прилета', 'Дата и время вылета', 'Дата и время прилета']
                return render_template('flight_number_result.html', schema=list_name, result=flight_number_result)
        else:
            return render_template('flight_number_form.html', error_message="Введите данные")


@blueprint_query.route('/task2', methods=['GET', 'POST'])
@login_required
@group_required
def task2():
    if request.method == 'GET':
        return render_template('sum_cost_form.html')
    else:
            input_year = request.form.get('input_year')
            if input_year:
                _sql = provider.get('sum_cost_for_year.sql', input_year=input_year)
                year_result, schema = select(current_app.config['db_config'], _sql)
                if not year_result:
                    return render_template('sum_cost_form.html', error_message="Данных не найдено")
                else:
                    list_name = ['Год', 'Сумма']
                    return render_template('sum_cost_for_years_result.html', schema=list_name, result=year_result)
            else:
                return render_template('sum_cost_form.html', error_message="Введите данные")


@blueprint_query.route('/task3', methods=['GET', 'POST'])
@login_required
@group_required
def task3():
    if request.method == 'GET':
        return render_template('info_of_sale_tickets_form.html')
    else:
            input_year= request.form.get('input_year')
            input_month = request.form.get('input_month')
            if input_year and input_month:
                _sql = provider.get('info_of_sale_ticket.sql', input_year=input_year, input_month=input_month)
                info_result, schema = select(current_app.config['db_config'], _sql)
                if not info_result:
                    return render_template('info_of_sale_tickets_form.html', error_message="Данных не найдено")
                else:
                    list_name = ['Номер билета', 'Цена', 'Дата продажи', 'Название рейса']
                    return render_template('info_of_sale_tickets_result.html', schema=list_name, result=info_result)
            else:
                return render_template('info_of_sale_tickets_form.html', error_message="Введите данные")