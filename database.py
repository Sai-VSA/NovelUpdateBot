import mysql.connector
from mysql.connector import Error
##import pandas as pd

def create_db_connection(host_name, user_name, user_password, db_name, prt):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port = prt,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
     #   print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

create_data_table = """
CREATE TABLE book_table (
  book_id VARCHAR(200),
  latest_chap INT
  );
 """

connection = create_db_connection("priestbooks.cjuo8kiim0gz.us-east-2.rds.amazonaws.com", "#####", "########", "books", "3306")
##create_database_query = "CREATE DATABASE books"
##create_database(connection, create_database_query)

#execute_query(connection, create_teacher_table) 

def add_recent(url, num):

 q1 = """
  UPDATE book_table
  SET latest_chap = """ + str(num) + """ 
  WHERE book_id = '""" + url + "'"
 execute_query(connection, q1)

def add_to_table(url):
  q1 = """
  SELECT latest_chap
  FROM book_table
  WHERE book_id =  '""" + url + "'"
  results = read_query(connection, q1)
  
  if not(results):
    push_book = """
    INSERT INTO book_table 
    VALUES ('""" + url +  "', " + "0" + ")"
    execute_query(connection, push_book)

def return_recent(url):
  q1 = """
  SELECT latest_chap
  FROM book_table
  WHERE book_id = '""" + url + "'"
  results = read_query(connection, q1)
  
  for result in results:
    return int(result[0])
  