__author__ = 'Harshini Bonam'

import psycopg2

def main():
    #try:
        connection = psycopg2.connect(database="postgres", user="postgres", password="12345", host="127.0.0.1", port="5432")
        print "\nDB connection opened succesfully"
    #except:
    #    print "ERROR: Connection cannot be done."

    #try:
        cursor = connection.cursor()
        print "\nCreated cursor."
        cursor.execute('''create table sampleDB ( itemID serial, users text[], primary key(itemID));''')
        cursor.execute('''insert into sampleDB (users) values ('{"hi", "hello"}');''')
        cursor.execute('''select * from sampleDB;''')
        rows = cursor.fetchall()
        for row in rows:
            print "ITEM : ", row[0]
            print "USERS Ratings : ", row[1]
        connection.close()
    #except:
    #    print "\nERROR: Cannot execute query."





main()