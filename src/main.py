import datetime
import re
import psycopg2
import logging
from sample import config,create_db_if_not_exits
from decimal import Decimal
from  flask import Flask, render_template,request,redirect,url_for,jsonify


app = Flask(__name__)

file_path ="file.txt"  #path of the file



#Ensuring the database is connected
def connect():
    conn = None
    try:
        create_db_if_not_exits()
        params = config()
        print('Connecting to Postgres ...')
        conn = psycopg2.connect(**params)
        return conn
    except Exception as e:
        print(e)
        return None
    # finally:
    #     if conn is not None:
    #         conn.close()
    #         print("Database connection closed ")

def initialize_database():
    conn = connect()

    try:
        cursor  =  conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Main_Summary(
                summary_id SERIAL PRIMARY KEY,
                summary_date DATE NOT NULL)
            """
        )

        cursor.execute ("""
            CREATE TABLE IF NOT EXISTS Expense_type (
                type_id SERIAL PRIMARY KEY,
                expense_type_name TEXT)
        
         """)
        cursor.execute ("""
            CREATE TABLE IF NOT EXISTS Expense(
                expense_id SERIAL PRIMARY KEY,
                summary_id INT REFERENCES Main_Summary(summary_id),
                type_id INT REFERENCES Expense_type(type_id),
                amount DECIMAL(10,2) NOT NULL,
                description TEXT)

         """)

        expense_types = ['Food','Personal','Savings','Bills','other']
        for  expense_type in expense_types:
            cursor.execute(
                "INSERT INTO Expense_type ( expense_type_name) SELECT %s WHERE NOT EXISTS (SELECT 1 FROM Expense_type WHERE expense_type_name =%s) ",(expense_type,expense_type))
            conn.commit()
            print("Database initialised sucessfully .. ")
        return True

    except Exception as e :
        conn.rollback()
        print(f"There is a error from initialize_database that is {e}")
        return False
    finally:
        conn.close()

def parse_expense_line(line):
    line = line.lower().strip()

    expense_types = ['Food','Personal','Savings','Bills']
    expense_type = next((x for x in expense_types if x in line ),'Other')
    
    
    amount_match = re.search(r'-\s*([\d.]+)\s*-',line)


    if not amount_match:
        print(f"No expense found it the line : {line}")
        return None 
    
    amount = Decimal(amount_match.group(1))


    date_match = re.search(r'(\d{2}/\d{2}/\d{2})',line)

    if date_match:
        date_str =  date_match.group(1)
        date = date_str.replace('/','-')
    else:
        date = datetime.datetime.now().strftime('%d-%m-%y')
    return{
        'type':expense_type,
        'amount':amount,
        'date':date,
    }
def database_main_insertion(data):
    conn = connect()
    cursor =  conn.cursor()
    try:
        cursor.execute('INSERT INTO Main_Summary(summary_date) SELECT %s WHERE NOT EXISTS (SELECT 1 FROM Main_Summary WHERE summary_date=%s) RETURNING summary_id ',(data['date'],data['date']))
        summary_insert_result = cursor.fetchone()

        if summary_insert_result:
            main_summary_id = summary_insert_result[0]
        else:
            cursor.execute('SELECT summary_id FROM Main_Summary WHERE summary_date =%s',(data['date'],))
            main_summary_id = cursor.fetchone()[0]

        
        cursor.execute('INSERT INTO Expense_type (expense_type_name) SELECT %s WHERE NOT EXISTS (SELECT 1 FROM Expense_type WHERE expense_type_name =%s) RETURNING type_id ',(data['type'],data['type']))
        expense_type_result = cursor.fetchone()

        if expense_type_result:
            expense_type_id = expense_type_result[0]
        else:
            cursor.execute('SELECT type_id FROM Expense_type WHERE expense_type_name=%s ',(data['type'],))
            expense_type_id = cursor.fetchone()[0]        
             
        cursor.execute('INSERT INTO Expense (summary_id,type_id,amount,description) VALUES (%s,%s,%s,NULL)',(main_summary_id,expense_type_id,data['amount'],))
        conn.commit()


    except Exception as e:
        conn.rollback()
        print(f"Error from database_main_insertion : {e}")
    finally:
        conn.close()





def details():
    conn = connect()
    cursor =  conn.cursor()
    try:
        cursor.execute('SELECT * FROM Expense')
        results = cursor.fetchall()
        for row in results:
            print(row)
        conn.close()
    except Exception as e:
        print(f"{e}")
    finally:
        conn.close()
def main():

    if initialize_database():
        print("Database initialized successfully ")
        with open(file_path,'r') as f:
            file =  f.readlines()
        print(file)
        total_processed =0
        for line in file:
            expense_data =  parse_expense_line(line)
            if expense_data :
                database_main_insertion(expense_data)
                total_processed+=1
        print(f"Processed {total_processed} expenses from {file_path}")

        print("Showing the expenses : ")
        details()
    else:
        print("Failed ")

if __name__ == '__main__':
    main()







    --- front

    --- server file 
        - listens to a port
        - routes requests
        - calls controller (logic)


    --- logic (controller)