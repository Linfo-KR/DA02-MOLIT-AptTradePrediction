import pymysql
import logging


def connect_db(dbName):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='4303', charset='utf8')
        cursor = conn.cursor()
        
        cursor.execute(f"SHOW DATABASES LIKE '{dbName}'")
        dbCheck = cursor.fetchone()
        
        if not dbCheck:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName}")
            conn.commit()
            print(f'[CREATE DATABASE] => MySQL DATABASE [{dbName}]')
            
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='4303', db=dbName, charset='utf8')
        if conn:
            print(f'[CONNECT DATABASE] => MySQL DATABASE [{dbName}]')
            
        cursor = conn.cursor()
        
        return conn, cursor
    
    except Exception as e:
        print(f'[CONNECT ERROR] => {e}')
        
        return None, None

def create_table_query(conn, cursor, tableName):
    try:
        cursor.execute(f"SHOW TABLES LIKE '{tableName}'")
        tableCheck = cursor.fetchone()
        
        if not tableCheck:
            query = f"""
                CREATE TABLE {tableName} (
                    year CHAR(4),
                    month VARCHAR(2),
                    day VARCHAR(2),
                    price VARCHAR(40),
                    code CHAR(5),
                    dong_name VARCHAR(40),
                    jibun VARCHAR(10),
                    con_year CHAR(4),
                    apt_name VARCHAR(40),
                    area VARCHAR(20),
                    floor VARCHAR(4)
                )
            """
            cursor.execute(query)
            conn.commit()
            print(f'[CREATE TABLE] => [{tableName}]')
        else:
            print(f'[EXISTED TABLE] => [{tableName}]')
    
    except Exception as e:
        print(f"[ERROR IN CREATE TABLE] => {e}")

def insert_query(conn, cursor, tableName, dataList):
    try:
        query = f"""
            INSERT INTO {tableName} (
                year, month, day, price, code, dong_name, jibun, con_year, apt_name, area, floor
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(query, dataList)
        conn.commit()
        
    except Exception as e:
        logging.error(f"[ERROR IN INSERT DATA] : {e}")