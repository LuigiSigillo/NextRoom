import logging
import pyodbc
import azure.functions as func
import json 
import os
import datetime
import requests

'''
can handle also this
log_list = {
    "board1": {
        "timestamp": "20200518",
        "list_devices": {
            "s8": "28",
            "iphonediNic": "48",
            "etc": "10"
        }
    },
    "board2": {
        "timestamp": "20200518",
        "list_devices": {
            "s8": "58",
            "iphonediNic": "18",
            "etc": "5"
        }
    }
}

but for now this is the log that arrive

single_log = {'room1':{'timestamp':'01-01-1970 00:00:40', 'list_devices':{'50:35:28:129:55':'39'}}}
    
'''

def main(event: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s', event.get_body().decode('utf-8'))
    log_list = json.loads(event.get_body().decode('utf-8')) 
    single_log = log_list[0]
    logging.info("%s", single_log)
    #get positions from the msg arrived from the boards
    new_positions = get_position_devices(single_log)

    # take from the db the previous positions
    previous_positions = retrieve_from_db_prev_positions()
    timestamp = reconstruct_timestamp(single_log)
    # find movements and update the db current visit and visit
    find_movements(new_positions, previous_positions, timestamp)
    
    
    logging.info("DONE!")




def reconstruct_mess(msg):
    pass #{'b1': {'ts': '01-01-1970 00:50:21', 'l_d': {'s8': '28', 'i': '37'}}}

def reconstruct_timestamp(single_log):
    #TODO room1 need to be room+i 
    datetime_str = single_log["room1"]["timestamp"] #"01-01-1970 00:21:38"
    #logging.info("%s",(single_log["room1"]["timestamp"]))
    datetime_object = datetime.datetime.strptime(datetime_str, '%m-%d-%Y %H:%M:%S')
    return datetime_object

#================================ UTILITY.py =============================================


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

def insert_row(table,device,room,value,update): #value could be timestamp or duration depednding on table
    #TODO need to manipulate room parameter EX paramter room=board1 --> room1 etc.
    conn = connect_to_db()
    cursor = conn.cursor()
    if update:
        update_string = "UPDATE "+table + " SET " + room + "= ? WHERE device_id = ?"
        cursor.execute(update_string, value, device)
    elif table != "dbo.People":
        insert_string = "INSERT INTO " + table + " (device_id, " + room + ") "+ "VALUES (?,?);"
        cursor.execute(insert_string,device,value)
    else:
        #value è una lista di quante persone sono nelle stanze
        #dev qui è il timestamp
        insert_string = "INSERT INTO " + table + " (time_stamp, room1,room2,room3, room4, room5,room6,room7, room8, room9, room10, room11,room12,room13, room14, room15,room16,room17, room18, room19, room20) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
        cursor.execute(insert_string, device,value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8],value[9],value[10],value[11],value[12],value[13],value[14],value[15],value[16],value[17],value[18],value[19],value[20])
    try:
        conn.commit()
    except e:
        logging.info("error", e)

    logging.info("row successfully added")
    conn.close()

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


def get_distance_other_rooms(msg_examples,board,dev):
    min_ = {}
    for b in msg_examples:
        if b == board:
            continue
        else:
            if dev in msg_examples[b]['list_devices']:
                min_[b] =  msg_examples[b]['list_devices'][dev]
    return min_


def get_position_devices(msg_examples):
    positions = {}
    for board in msg_examples:
        for dev in msg_examples[board]['list_devices']:
            if dev not in positions:
                distance_other_rooms = get_distance_other_rooms(msg_examples,board,dev)
                if distance_other_rooms != {}:
                    min_room = min(distance_other_rooms.keys(), key=distance_other_rooms.get)
                    if msg_examples[board]['list_devices'][dev] < msg_examples[min_room]['list_devices'][dev]:
                        positions[dev] = board
                else: #only present in one room so the distance is  the one of the only room it is present in
                    positions[dev] = board
    return positions


def get_visit_id(dev_id):
    query = "SELECT visit_id from [dbo].[CurrentVisits] where device_id = '" + dev_id + "'"
    lst = query_db(query)
    visits_id = []
    for row in lst:
        visits_id.append(int(row[0]))
    return max(visits_id)

def get_duration(dev,old_pos,timestamp):
    # get timestamp of the previous visit from the currentvisit table
    # do the difference betwewen curr_ts and prev_ts = time spent
    # insert value in visits table
    vis_id = get_visit_id(dev)
    select_string = "SELECT " + old_pos +" FROM dbo.CurrentVisits WHERE device_id ='" + dev + "' and visit_id=" + str(vis_id)
    old_timestamp = query_db(select_string)[0][0]
    duration_delta = timestamp - old_timestamp
    duration = duration_delta.seconds // 60
    return duration


def detected_new_room(dev,old_pos,new_pos,timestamp):
    #insert the duration of the previous room in the visits table
    logging.info("device: %s oldpos: %s tiestamp; %s",dev,old_pos, timestamp)
    dur = get_duration(dev,old_pos,timestamp)
    insert_row("dbo.Visits", dev, old_pos, dur, True)
    #insert row in current visit with timestamp to start the counter of the new room
    insert_row("dbo.CurrentVisits", dev, new_pos, timestamp, True)


def find_movements(new_positions, previous_positions,timestamp): #timestamp present in the msg_examples
    for dev in new_positions:
        if dev in previous_positions:
            if new_positions[dev] != previous_positions[dev]:
                detected_new_room(dev, previous_positions[dev], new_positions[dev], timestamp)
                generate_and_send_sugg(dev,new_positions)
        else:
            # detected new visitor
            insert_row("dbo.CurrentVisits", dev, new_positions[dev], timestamp, False)


def retrieve_from_db_prev_positions(): 
    positions = {}
    q_string = "SELECT * FROM dbo.CurrentVisits"
    rows = query_db(q_string)
    cur_room = ""
    for row in rows:
        max_ts = datetime.datetime(1998, 3, 30, 7, 14, 48, 237000)
        for i,ts in enumerate(row):
            if i> 1 and ts != None:
                #print("room = ",i-1,"\t",ts,"\n")
                if max_ts < ts:
                    max_ts = ts
                    cur_room = "room" + str(i-1)
        if cur_room !=  "":        
            positions[row[1]] = cur_room
    return positions




def count_people_in_rooms(positions):
    print("ecco le posizioni:",positions)
    counter = [0 for x in range(21)] #max 20 rooms in museum
    for dev in positions:
        idx = int(positions[dev][-1])
        counter[idx] = counter[idx] + 1
    insert_row("dbo.People", datetime.datetime.now(), None, counter, False)
    return counter


# ============================ GENERATE_SUGGESTIONS.py =======================================
# do all utente la lista ordinata dal piu grande al piu piccolo della visita del min(score)
# EX "v1": [10, 20, 2, 30] ---> "v1": [4, 2, 1, 3] (stanze)

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
            exists = current_visit[room]
        except:
            suggested_visit[room] = minutes

    suggestions = sorted(suggested_visit.keys(), key=suggested_visit.get, reverse=True)
    people_in_rooms = count_people_in_rooms(new_positions)
    
    for i,num_of_p in enumerate(people_in_rooms):
        if num_of_p > 15 and "room"+str(i) in suggestions:
            suggestions.remove("room"+str(i))

    return suggestions

def retrieve_curr_visit(device_id):
    #device_id = 's10'
    curr_visit = {}
    query = query_db("SELECT * FROM dbo.Visits WHERE device_id = '" + device_id + "'")
    for row in query:
            for i,col in enumerate(row):
                if i>1 and col != None:
                    curr_visit["room"+str(i-1)] = col
    print(curr_visit)
    return curr_visit
    





def generate_and_send_sugg(device_id, new_positions):
    last_visits = convert_in_json(device_id)
    current_visit = retrieve_curr_visit(device_id) 
    #current_visit ={'room1': 2, 'room4': 20}
    visit_id = get_visit_id(device_id)
    #do a post to the website with the current visit id
    url = 'http://localhost:3000/'
    myobj = {'visitid': visit_id, 'sugg_list': calculate_suggestions(last_visits,current_visit, new_positions)}

    x = requests.post(url, data = myobj)

    #logging.info("%s",x.text)