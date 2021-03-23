import json
import mysql.connector
import logging
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(filename='db.log', 
                    level=logging.INFO, 
                    format=f'%(asctime)s - %(name)s - %(threadName)s - %(message)s')


mydb = mysql.connector.connect(
    host="mysqlContainer",
    user=os.environ.get("userDB"),
    password=os.environ.get('passwordBD'), 
    database= os.environ.get('database')
                )
                
mycursor = mydb.cursor()


class MyDB: 

    logging.info("connecting to the database: start")

    def __init__(self):
        self.mydb = mysql.connector.connect(
                    host="mysqlContainer", 
                    user="root",
                    password="password", 
                    database= "learning",
                )

        self.mycursor = self.mydb.cursor()
        self.list_tables = []
        self.data_dict = {}

    logging.info("connecting to the database: end")
    
    def get_tables(self):

        logging.info("Getting tables: start")

        with open('links.json') as json_data:
            self.data_dict = json.load(json_data)
        for i in self.data_dict:
            self.list_tables.append(i)

        logging.info("Getting tables: end")

    def create_table(self):

        logging.info("creating table: start")

        for i in self.list_tables:
            sql = "CREATE TABLE IF NOT EXISTS {} (ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), chaine VARCHAR(100), url TEXT, description TEXT);".format(i)
            self.mycursor.execute(sql)

        logging.info("creating table: end")

    def insert_table(self):

        logging.info("inserting into table: start")

        for i in self.data_dict.items():

            categorie = i[0]

            for y in i[1]:
                val = tuple(y.values())
                db_key = ", ".join(y.keys())
                sql = "INSERT INTO {} ({}) VALUES {};".format(categorie, db_key, val)
                
                self.mycursor.execute("USE learning;")
                self.mycursor.execute(sql)
                self.mydb.commit()

        logging.info("inserting into table: end")


mydb = MyDB()
mydb.get_tables()
mydb.create_table()
mydb.insert_table()
