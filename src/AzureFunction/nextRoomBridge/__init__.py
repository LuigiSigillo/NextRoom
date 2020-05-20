import logging
import pyodbc
import azure.functions as func
import json 
import os




def main(event: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s', event.get_body().decode('utf-8'))
    log_list = json.loads(event.get_body().decode('utf-8')) 
    single_log = log_list[0]
    logging.info("%s",single_log)
        

        
def connect_to_db():
    server = 'webappacc.database.windows.net'
    database = 'NextRoom'
    username = 'luigi'
    password = os.environ.get('dbPWD')
    driver= '{ODBC Driver 17 for SQL Server}'
    logging.info("tryng to coonnect")
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    logging.info("connected")
    return cnxn

def insert_row():
    conn = connect_to_db()
    cursor = conn.cursor()
    insert_string = "INSERT INTO dbo.Accelerometer (x, y, z, IsMoving, DateOfArrival) OUTPUT INSERTED.Id VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP);"
    cursor.execute(insert_string, x, y, z, is_moving)
    try:
        conn.commit()
    except e:
        logging.info("error", e)
    logging.info("row successfully added")
    conn.close()




