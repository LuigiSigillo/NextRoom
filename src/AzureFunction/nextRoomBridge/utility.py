import logging
import pyodbc
import azure.functions as func
import json 
import os
import datetime
import array

msg_examples = {
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
    },
    "board3": {
        "timestamp": "20200518",
        "list_devices": {
        }
    },
    "board4": {
        "timestamp": "20200518",
        "list_devices": {
        }
    },
    "board5": {
        "timestamp": "20200518",
        "list_devices": {
        }
    }
}

'''
detect spostamento da 1 a 2
int tempospeso = now-get.id.getroom1
insert vistid room1=te nella table visits
insert current_timestamp in room2 table currentvisits
'''

def connect_to_db():
    server = 'webappacc.database.windows.net'
    database = 'NextRoom'
    username = 'luigi'
    password = "nextRoom1"#os.environ.get('dbPWD')
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
    return positions


def get_duration(dev,old_pos,timestamp):
    # get timestamp of the previous visit from the currentvisit table
    # do the difference betwewen curr_ts and prev_ts = time spent
    # insert value in visits table
    select_string = "SELECT " + old_pos +" FROM dbo.CurrentVisits WHERE device_id ='" + dev + "'"
    old_timestamp = query_db(select_string)[0][0]
    duration = timestamp - old_timestamp
    return duration


def detected_new_room(dev,old_pos,new_pos,timestamp):
    #insert the duration of the previous room in the visits table
    dur = get_duration(dev,old_pos,timestamp)
    insert_row("dbo.Visits", dev, old_pos, dur, True)
    #insert row in current visit with timestamp to start the counter of the new room
    insert_row("dbo.CurrentVisits", dev, new_pos, timestamp, True)


def find_movements(new_positions, previous_positions,timestamp): #timestamp present in the msg_examples
    for dev in new_positions:
        if dev in previous_positions:
            if new_positions[dev] != previous_positions[dev]:
                detected_new_room(dev, previous_positions[dev], new_positions[dev], timestamp)
        else:
            # detected new visitor
            insert_row("dbo.CurrentVisits", dev, room, timestamp, False)


def retrieve_from_db_prev_positions(): 
    positions = {}
    q_string = "SELECT * FROM dbo.CurrentVisits"
    rows = query_db(q_string)
    for row in rows:
        max_ts = datetime.datetime(1998, 3, 30, 7, 14, 48, 237000)
        for i,ts in enumerate(row):
            if i> 1 and ts != None:
                print("room = ",i-1,"\t",ts,"\n")
                if max_ts < ts:
                    max_ts = ts
                    cur_room = "room" + str(i-1)
                
        positions[row[1]] = cur_room
    return positions




def count_people_in_rooms(positions):
    counter=verts = [0 for x in range(21)] #max 20 rooms in museum
    for dev in positions:
        idx = int(positions[dev][-1])
        counter[idx] = counter[idx] +1
    insert_row("dbo.People", datetime.datetime.now(), None, counter, False)
    return counter
#get positions from the msg arrived from the boards
new_positions = get_position_devices(msg_examples)

# take from the db the previous positions
previous_positions = retrieve_from_db_prev_positions()

# find movements and update the db current visit and visit
find_movements(new_positions, previous_positions, timestamp)

