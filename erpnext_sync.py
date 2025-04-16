import mysql.connector
import local_config as config
import requests
import json
from datetime import date
import datetime
import calendar


ERPNEXT_VERSION = getattr(config, 'ERPNEXT_VERSION', 14)

class Epush:
    def dbConnect(self):
        current_month, current_year = datetime.datetime.today().month, datetime.datetime.today().year
        _,num_days = calendar.monthrange(current_year, current_month)
        start_date, end_date = datetime.datetime(current_year, current_month, 1).strftime("%m/%d/%Y"), datetime.datetime(current_year, current_month, num_days).strftime("%m/%d/%Y")
        today_date = date.today()
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="epushserver"
            )
        mycursor = mydb.cursor(dictionary=True)
        # Current Date SQL_Query
        query = '''select UserId,LogDate,Direction,DeviceId from devicelogs_processed where DATE(LogDate) = '{0}' '''.format(today_date)
        # Month start date to end date SQL_Query
        # query = '''select UserId,LogDate from DeviceLogs_{0}_{1} where LogDate >= #{2}# and LogDate <= #{3}# '''.format(current_month,current_year,start_date,end_date)
        # query = '''select UserId,LogDate from DeviceLogs_11_2022 where LogDate >= #11/9/2022# and LogDate <= #11/17/2022# '''
        mycursor.execute(query)
        print("Query executed")
        fetch_data = mycursor.fetchall()
        print(fetch_data)
        endpoint_app = "hrms" if ERPNEXT_VERSION > 13 else "erpnext"
        url = f"{config.ERPNEXT_URL}/api/method/{endpoint_app}.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field"
        headers = {
            'Authorization': "token "+ config.ERPNEXT_API_KEY + ":" + config.ERPNEXT_API_SECRET,
            'Accept': 'application/json'
        }
        for data in fetch_data:
            print(data)
            data = {
                'employee_field_value' : data['UserId'],
                'timestamp' : data['LogDate'].strftime('%y-%m-%d %H:%M:%S'),
                'device_id' : data['DeviceId'],
                'log_type' : 'IN' if data['Direction'] == 'in' else 'OUT'
            }
            try:
                response = requests.request("POST", url, headers=headers, json=data)
            except Exception as e:
                print("Biometric attendance update failed: ",e)
            print(json.loads(response._content))

obj = Epush()
obj.dbConnect()
