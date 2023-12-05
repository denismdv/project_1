import datetime
from psycopg2 import Error
import psycopg2
import sqlite3
from sqlite3 import Error
from abc import abstractmethod, ABC
import pandas as pd


class DataClient(ABC):
    @abstractmethod
    def _get_connection(self):
        pass
    
    @abstractmethod
    def create_mebel_table(self, conn):
        pass
    
    @abstractmethod
    def insert_items(self, conn, url, price, description):
        pass
    
    @abstractmethod
    def get_items(self, conn, price_from=0, price_to=100000):
        pass
    
    def run_test(self):
        with self._get_connection():
            self.create_mebel_table()
            items = self.get_items(10, 100)
            for item in items:
                print(item)


class PostgresClient(DataClient):
    USER = "postgres"
    PASSWORD = "postgres"
    HOST = "127.0.0.1"
    PORT = "5432"
    def _get_connection(self):
        return psycopg2.connect(
                user=self.USER,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT
                            )
            
    def create_mebel_table(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS app_1_mebel(
                            id serial PRIMARY KEY,
                            link text,
                            price integer,
                            description text
                        )
                        """)
        
    def insert_items(self, url, price, description):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO app_1_mebel(link, price, description, parse_date_time) VALUES ('{url}', '{price}', '{description}', '{datetime.datetime.now()}')")
        
    def get_items(self, price_from=0, price_to=100000):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM app_1_mebel WHERE price >= {price_from} and price <= {price_to}")
            return cursor.fetchall()
    
    
class SqliteClient(DataClient):
    DB_NAME = "parsing/kufar.db"
    def _get_connection(self):
           return sqlite3.connect(self.DB_NAME)
            
    def create_mebel_table(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS mebel(
                            id integer PRIMARY KEY autoincrement,
                            url text,
                            price integer,
                            description text
                        )
                        """)
        
    def insert_items(self, link, price, description):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO mebel(url, price, description) VALUES ('{link}', '{price}', '{description}')")
        
    def get_items(self, price_from=0, price_to=100000):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM mebel WHERE price >= {price_from} and price <= {price_to}")
            return cursor.fetchall()
    

class CsvClient(DataClient):
    CSV_NAME = "mebel.csv"
    mebel_items = []
    def _get_connection(self):
        pass
            
    def create_mebel_table(self):
        pass
        
    def insert_items(self, url, price, description):
        self.mebel_items.append([url, price, description])
        df = pd.DataFrame(self.mebel_items, columns=["Ссылка", "Цена", "Описание"])
        df.to_csv(self.CSV_NAME, index=False, encoding="utf-8")
        
    def get_items(self, price_from=0, price_to=100000):
        df = pd.read_csv(self.CSV_NAME)
        res = df[(df["Цена"] <= price_to) & (df["Цена"] >= price_from)].values.tolist()
        return res
    

# data_client = CsvClient()
# data_client.run_test()
