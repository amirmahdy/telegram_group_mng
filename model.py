import mysql.connector as mariadb
from config import db_pass, db_db, db_user


def register_user(user_id, user_name, user_place):
    mariadb_connection = mariadb.connect(user=db_user, password=db_pass, database=db_db)
    cursor = mariadb_connection.cursor()
    sql = "INSERT INTO users (id, name, place) VALUES (%s, %s, %s)"
    val = (user_id, user_name, user_place)
    cursor.execute(sql, val)
    mariadb_connection.commit()
    cursor.close()
    mariadb_connection.close()
