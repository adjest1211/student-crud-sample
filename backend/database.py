import mysql.connector

def dbconnect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ionic_crud_db",
        port="3306"
    )