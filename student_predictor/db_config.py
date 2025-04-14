import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Samarth@2004",
        database="student_db",
        auth_plugin="mysql_native_password")
