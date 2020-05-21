import pyodbc
import datetime

def connect_to_db():
    server = '<server>.database.windows.net'
    database = '<databaseName>'
    username = '<DBadmin>'
    password = 'DBpassword'
    driver= '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn

def query_db(query_string):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query_string)
    row = cursor.fetchone()
    while row:
        print (str(row[0]) + " " + str(row[1]))
        row = cursor.fetchone()
    conn.close()

def insert_row():
    conn = connect_to_db()
    cursor = conn.cursor()
    name = "SQL Server Express 201467"
    number = "SQLEXPRESS201567"
    cost = 11
    price = 11
    insert_string = "INSERT INTO SalesLT.Product (Name, ProductNumber, StandardCost, ListPrice, SellStartDate) OUTPUT INSERTED.ProductID VALUES (?, ?, ?, ?, ?);"
    try:
        cursor.execute(insert_string, name, number, cost, price, datetime.datetime.now())
    except:
        print("an error occurred")
    conn.commit()
    print("row successfully added")
    conn.close()

def delete_row():
    conn = connect_to_db()
    cursor = conn.cursor()
    delete_string = "DELETE FROM SalesLT.Product WHERE Name=?"
    name = "SQL Server Express 201467"
    try:
        cursor.execute(delete_string, name)
    except:
        print("an error occurred during the deletion")
    conn.commit()
    print("rows successfully deleted")
    conn.close()

def create_schema():
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE SCHEMA BigProject")
    except:
        print("an error occurred during the creation of the schema")
        return
    conn.commit()
    print("schema successfully created")
    conn.close()

def create_table():
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE BigProject.userdata (col1 INT PRIMARY KEY)")
    except:
        print("an error occurred during the creation of the table")
        return
    conn.commit()
    print("table successfully created")
    conn.close()

def drop_table():
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE nextroomDB.BigProject.userdata")
    except:
        print("an error occurred during the dropping of the table")
        return
    conn.commit()
    print("table successfully dropped")
    conn.close()


#Sample query string
#query_string = "SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName FROM [SalesLT].[ProductCategory] pc JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid"
query_string = "SELECT * FROM [SalesLT].[Product]"
#query_db(query_string)

#insert_row()

#delete_row()

#query_db(query_string)
drop_table()





