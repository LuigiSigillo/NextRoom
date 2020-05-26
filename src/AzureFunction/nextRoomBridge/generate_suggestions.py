# do all utente la lista ordinata dal piu grande al piu piccolo della visita del min(score)
# EX "v1": [10, 20, 2, 30] ---> "v1": [4, 2, 1, 3] (stanze)

import pyodbc
import logging

""" 
#hard coded visits
last_visits = {"v1": {
                    'room1': 10, 
                    'room2': 20,
                    'room3': 2, 
                    'room4': 30
                    }, 
                "v2": {
                    'room1': 0, 
                    'room2': 5,
                    'room3': 23, 
                    'room4': 1
                    }
}
 """

def connect_to_db():
    server = 'webappacc.database.windows.net'
    database = 'NextRoom'
    username = 'luigi'
    password = ""
    driver= '{ODBC Driver 17 for SQL Server}'
    logging.info("tryng to coonnect")
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    logging.info("connected")
    return cnxn


def query_db(query_string):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query_string)
    row = cursor.fetchone()
    lst = []
    while row:
        lst.append(row)
        row = cursor.fetchone()
    conn.close()
    return lst

def convert_in_json(device_id):
    query = query_db("SELECT * FROM dbo.Visits WHERE device_id != '" + device_id + "'")
    last_visits = {}
    for row in query:
        for i,col in enumerate(row):
            if i == 0:
                last_visits[col] = {}
                curr_v = col
            elif i>1 and col != None:
                last_visits[curr_v]["room"+str(i-1)] = col
    print(last_visits)
    return last_visits


def calculate_suggestions(last_visits, current_visit):
    score = {}

    for visit_id, visit in last_visits.items():
        score[visit_id] = 0
        for room, minutes in current_visit.items():
            score[visit_id] += abs(current_visit[room] - visit[room])

    min_score = min(score.keys(), key=score.get)

    best_visit = last_visits[min_score]

    suggested_visit = {}

    for room, minutes in best_visit.items():
        try:
            current_visit[room]
        except:
            suggested_visit[room] = minutes

    suggestions = sorted(suggested_visit.keys(), key=suggested_visit.get, reverse=True)
    print(suggestions)
    return suggestions

def retrieve_curr_visit(device_id):
    device_id = 's10'
    curr_visit = {}
    query = query_db("SELECT * FROM dbo.Visits WHERE device_id = '" + device_id + "'")
    for row in query:
            for i,col in enumerate(row):
                if i>1 and col != None:
                    curr_visit["room"+str(i-1)] = col
    print(curr_visit)
    return curr_visit
    


last_visits = convert_in_json(device_id="s10")
current_visit = retrieve_curr_visit(device_id="s10") 
current_visit ={'room1': 2, 'room4': 20}
#calculate_suggestions(last_visits, current_visit)

#do a post to the website with the current visit id

import requests

url = 'http://localhost:3000/'
myobj = {'visitid': 12, 'sugg_list': calculate_suggestions(last_visits,current_visit)}

x = requests.post(url, data = myobj)

print(x.text)