import sys
import sqlite3
from TextParser import BusinessCardParser


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def insertVaribleIntoTable(name, email, phone, address):
    global sqliteConnection
    try:
        database = r"database/pythonsqlite.db"
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()

        print("Connected to SQLite")

        sql_insert_table = """ INSERT INTO cards (name, email_id, phone_number, address) 
                            VALUES (?, ?, ?, ?); """

        data_tuple = (name, email, phone, address)
        cursor.execute(sql_insert_table, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def delete_user(name):
    """
    Delete a task by task id
    :param name:
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """

    database = r"database/pythonsqlite.db"
    sqliteConnection = sqlite3.connect(database)
    sql = """ DELETE FROM cards WHERE name=?; """
    cur = sqliteConnection.cursor()
    cur.execute(sql, (name,))
    sqliteConnection.commit()


def parseInput():
    input = open(sys.argv[1], "r")
    total = input.read()
    print(total)

    # parse file
    bcp = BusinessCardParser()
    ci = bcp.getContactInfo(total)

    print("==>\n")

    print("Name:", ci.getName)
    print("Phone:", ci.getPhoneNumber)
    print("Email:", ci.getEmailAddress)


def main():
    if len(sys.argv) != 2:
        print("usage:", sys.argv[0], "<filename>")
        return 1
    # read from file
    input = open(sys.argv[1], "r")
    total = input.read()
    print(total)

    # parse file
    bcp = BusinessCardParser()
    ci = bcp.getContactInfo(total)

    print("==>\n")

    print("Name:", ci.getName)
    print("Phone:", ci.getPhoneNumber)
    print("Email:", ci.getEmailAddress)

    insertVaribleIntoTable(ci.getName, ci.getEmailAddress, ci.getPhoneNumber)


if __name__ == '__main__':
    main()
