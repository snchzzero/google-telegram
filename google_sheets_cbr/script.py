# для google_API
from pprint import pprint
import httplib2
from googleapiclient import discovery  # вместо apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# для db_google_sheets
import psycopg2
from google_sheets_cbr.config_db import host, user, password, db_name
import requests
import xmltodict

from GoogleSheetsCBR.models import Models
# для логов
from datetime import datetime
import sys
import time
import sys
#
#
# функция чтения гугл таблицы
def google_API():
    # подключение API

    CREDENTIALS_FILE = 'creds.json'  # файл с API
    spreadsheet_id2 = '1Ua9FHQRGdXNBgt6DH1pnG6slaU3nRFOlrCNfdV4ew1A'  # из url схемы таблицы гугл
    spreadsheet_id = '1V-lsTLgKAZ7Kn90ARq3K84YsQxkD-h-mML2Xl0VATD8'  # из url схемы таблицы гугл (тестовое)

    # документы с которыми будем работать
    creadentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])

    # создаем объект аунтификации
    httpAuth = creadentials.authorize(httplib2.Http())

    # создаем обертку API из которой мы будем получать данные из нашей схемы (v4 версия API sheets)
    service = discovery.build('sheets', 'v4', http=httpAuth)

    # Читаем данные 'A1:aA10' - диапозон, если весь то range='Лист1'
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Лист1',
        majorDimension='ROWS').execute()
    # pprint(values)
    return (values)
    # exit()


# функция текущего курса доллара
def cbr_usd_api():
    day = datetime.now().strftime("%d")
    mounth = datetime.now().strftime("%m")
    year = datetime.now().strftime("%Y")
    url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{mounth}/{year}'
    xml = xmltodict.parse(requests.get(url).content)
    # print(xml)
    # print()
    # print(xml['ValCurs']['Valute'])
    for value in xml['ValCurs']['Valute']:
        if value['@ID'] == 'R01235':
            # print(value['Name'])
            return (value['Value'])


# функция записи данных в БД PostgreSQL
def db_google_sheets():
     try:
         # подключаемся к базе данных
         # создаем объект
         connection = psycopg2.connect(
             host=host,
             user=user,
             password=password,
             database=db_name
         )
         connection.autocommit = True  # что бы не писать после каждого запроса коммит

        # для работы с БД нужно создать объект курсор (для выполнения различных команд SQl)
         with connection.cursor() as cursor:
             cursor.execute("SELECT version();")
        #     print(f'Server version: {cursor.fetchone()}')  #методо fetchone() возращает либо значание либо None

         with connection.cursor() as cursor:
             cursor.execute("""
             DROP TABLE IF EXISTS test;""")
        #     print(f'[{now}]: Drop old table "test" successfully')

         with connection.cursor() as cursor:
             cursor.execute("""
             CREATE TABLE test(
             id serial PRIMARY KEY,
             number integer,
             order_number integer,
             value_dolar int,
             value_rub int,
             delivery_time date);""")

         values = google_API()

         usd = float(str(cbr_usd_api()).replace(',', '.'))
         #print(f'[{now}]: Dollar rate {usd} rub')
         for i in range(1, len(values['values'])):
             number = values['values'][i][0]
             order_number = values['values'][i][1]
             value_dolar = values['values'][i][2]
             value_rub = round(usd * int(value_dolar), 0)
             #delivery_time = values['values'][i][3]
             delivery_time = str(values['values'][i][3]).split('.')[2] + "." + \
                             str(values['values'][i][3]).split('.')[1] + "." + \
                             str(values['values'][i][3]).split('.')[0]
             with connection.cursor() as cursor:
                 cursor.execute("""
                 INSERT INTO test (number, order_number, value_dolar, value_rub, delivery_time) VALUES
                 (%s, %s, %s, %s, %s);""", [int(number), int(order_number),
                                            int(value_dolar), value_rub, delivery_time])
         #print(f'Insert values into table "test" successfully')

     except Exception as _ex:
         pass
         #print(f'[{now}]: Error while working with PostgreSQL', _ex)
     finally:
         # закрываем подключение к БД
         if connection:
             connection.close()
             return (usd)




