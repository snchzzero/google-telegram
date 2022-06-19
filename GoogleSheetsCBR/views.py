from django.shortcuts import render, redirect
import psycopg2
from google_sheets_cbr.config_db import host, user, password, db_name
from google_sheets_cbr.script import db_google_sheets
from datetime import datetime
from .forms import Form_sort
import os



def home(request):
    # функция получения значений из гугл таблицы и курса доллара, автоматическое обновление таблицы
    usd = round(db_google_sheets(), 2)  # возвращает курс доллара

    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # получаем текущее время

    if request.method == 'GET':
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name)
            connection.autocommit = True  # что бы не писать после каждого запроса коммит

            # для работы с БД нужно создать объект курсор (для выполнения различных команд SQl)
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                #методо fetchone() возращает либо значание либо None
                a = cursor.fetchone()

            with connection.cursor() as cursor:
                cursor.execute("""
                SELECT number, order_number, value_dolar, value_rub, delivery_time FROM test""")
                rows = cursor.fetchall()
            return render(request, 'GoogleSheetsCBR/home.html',
                          {'form': Form_sort(),
                          'cursor': a, 'rows': rows, 'usd': usd, 'now': now})
        except ValueError:
            return render(request, 'GoogleSheetsCBR/home.html', {'error': 'Error while working with PostgreSQL'})
            # переданы неверные данные. попробуйте еще раз
        finally:
            # закрываем подключение к БД
            if connection:
                connection.close()

    elif request.method == 'POST':
        order_dict = {"№": "number", "Заказ, №": "order_number", "Стоимость": "value_dolar",
                      "Cрок поставки": "delivery_time "}
        ASC_DESK = {"возрастанию": 'ASC', "убыванию": 'DESC'}
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name)
            connection.autocommit = True  # что бы не писать после каждого запроса коммит

            # получаем данные из формы
            form = Form_sort(request.POST or None)
            if form.is_valid():
                data = form.cleaned_data.get("sorts_Model")
                ASC_DESK_data = form.cleaned_data.get("ASC_DESK_Model")
            else:
                data = "№"
                ASC_DESK_data = "возрастанию"
            s = "собака"
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                # print(f'Server version: {cursor.fetchone()}')  #методо fetchone() возращает либо значение либо None
                a = cursor.fetchone()

            with connection.cursor() as cursor:
                cursor.execute(f"""
                SELECT number, order_number, value_dolar, value_rub, delivery_time 
                FROM test 
                ORDER BY {order_dict[data]} {ASC_DESK[ASC_DESK_data]};""")
                rows = cursor.fetchall()
                return render(request, 'GoogleSheetsCBR/home.html', {'data': s, 'select': data,
                                                                     'ASC_DESK_data': ASC_DESK_data,
                                                                     'rows': rows, 'usd': usd,
                                                                     'now': now, 'cursor': a})

        except ValueError:
            return render(request, 'GoogleSheetsCBR/home.html', {'error': 'Error while working with PostgreSQL'})
        finally:
            # закрываем подключение к БД
            if connection:
                connection.close()

