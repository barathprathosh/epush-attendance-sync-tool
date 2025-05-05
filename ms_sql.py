import pyodbc
import local_config as config
import requests
import json
import datetime
ERPNEXT_VERSION = getattr(config, 'ERPNEXT_VERSION', 14)

# Connection details
server = 'ESSL\\SQLEXPRESS'      # e.g., 'localhost\\SQLEXPRESS' or '192.168.1.10'
database = 'eTimetracklite1'  # e.g., 'TestDB'
username = 'essl'       # e.g., 'sa'
password = 'essl'       # e.g., 'mypassword'

# Create the connection string
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

# Connect to SQL Server
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("Connected successfully.")
    
    current_month = datetime.datetime.today().month
    current_year = datetime.datetime.today().year

    table_name = f"DeviceLogs_{current_month}_{current_year}"
    # Example query
    
    # cursor.execute("SELECT DeviceId, UserId, LogDate,Direction FROM DeviceLogs_4_2025 ORDER BY LogDate DESC;")
    cursor.execute(f"SELECT DeviceId, UserId, LogDate,Direction FROM {table_name} ORDER BY LogDate DESC;")
    # cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'AttendanceLogs'")
    # cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    columns = [column[0] for column in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    endpoint_app = "hrms" if ERPNEXT_VERSION > 13 else "erpnext"
    url = f"{config.ERPNEXT_URL}/api/method/{endpoint_app}.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field"
    headers = {
        'Authorization': "token "+ config.ERPNEXT_API_KEY + ":" + config.ERPNEXT_API_SECRET,
        'Accept': 'application/json'
    }
    for data in rows:
        response = None
        direction = 'IN'
        if data.get("Direction"):
            direction = 'IN' if data['Direction'] == 'in' else 'OUT'
        data = {
            'employee_field_value' : data['UserId'],
            'timestamp' : data['LogDate'].strftime('%Y-%m-%d %H:%M:%S'),
            'device_id' : data['DeviceId'],
            'log_type' : direction
        }
        try:
            response = requests.request("POST", url, headers=headers, json=data)
        except Exception as e:
            print("Biometric attendance update failed: ",e)
        print(response)
        
    conn.close()

except Exception as e:
    print("Failed to connect:", e)
