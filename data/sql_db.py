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
            logging.info(f'[CREATE DATABASE] => MySQL DATABASE [{dbName}]')
            
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='4303', db=dbName, charset='utf8')
        if conn:
            logging.info(f'[CONNECT DATABASE] => MySQL DATABASE [{dbName}]')
            
        cursor = conn.cursor()
        
        return conn, cursor
    
    except Exception as e:
        logging.error(f'[CONNECT ERROR] => {e}')
        
        return None, None

def create_table_query(dbName, tableName):
    conn, cursor = connect_db(dbName)
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
            logging.info(f'[CREATE TABLE] => [{tableName}]')
        else:
            logging.info(f'[EXISTED TABLE] => [{tableName}]')
    
    except Exception as e:
        logging.error(f"[CREATE ERROR] => {e}")
    
    finally:
        cursor.close()
        conn.close()
 
def distinct_table_query(dbName, tableName):
    conn, cursor = connect_db(dbName)
    try:
        query = f"""
            SELECT COUNT(*) FROM {tableName};
        """
        cursor.execute(query)
        beforeDistinct = cursor.fetchone()[0]
        
        query = f"""
            CREATE TEMPORARY TABLE tbl_temp AS
            SELECT MIN(year) AS year, MIN(month) AS month, MIN(day) AS day, MIN(price) AS price, MIN(code) AS code, MIN(dong_name) AS dong_name, 
                    MIN(jibun) AS jibun, MIN(con_year) AS con_year, MIN(apt_name) AS apt_name, MIN(area) AS area, MIN(floor) AS floor
            FROM {tableName}
            GROUP BY year, month, day, price, code, dong_name, jibun, con_year, apt_name, area, floor;
        """
        cursor.execute(query)
        
        query = f"""
            DELETE FROM {tableName}
            WHERE NOT EXISTS (
                SELECT 1 FROM tbl_temp
                WHERE tbl_temp.year = {tableName}.year
                AND tbl_temp.month = {tableName}.month
                AND tbl_temp.day = {tableName}.day
                AND tbl_temp.price = {tableName}.price
                AND tbl_temp.code = {tableName}.code
                AND tbl_temp.dong_name = {tableName}.dong_name
                AND tbl_temp.jibun = {tableName}.jibun
                AND tbl_temp.con_year = {tableName}.con_year
                AND tbl_temp.apt_name = {tableName}.apt_name
                AND tbl_temp.area = {tableName}.area
                AND tbl_temp.floor = {tableName}.floor
            );
        """
        cursor.execute(query)
        conn.commit()
        
        query = f"""
            SELECT COUNT(*) FROM {tableName};
        """
        cursor.execute(query)
        afterDistinct = cursor.fetchone()[0]
        removeRows = beforeDistinct - afterDistinct
        
        logging.info(f'[DISTINCT DATA] => Removed : {removeRows} \t Remaining : {afterDistinct}')
        
    except Exception as e:
        logging.error(f'[ERROR] => {e}')
        
    finally:
        cursor.close()
        conn.close()
        
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
        logging.info(f'[INSERT DATA] => Successfully Inserted')
        
    except Exception as e:
        logging.error(f"[INSERT ERROR] : {e}")