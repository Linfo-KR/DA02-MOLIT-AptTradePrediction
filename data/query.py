import pymysql

from utils.utils import *


def connect_db(dbName):
    create_folder('./log')
    connectLogger = logger('connect_db', './log/connect_db.log')
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='4303', charset='utf8')
        cursor = conn.cursor()
        
        cursor.execute(f"SHOW DATABASES LIKE '{dbName}'")
        dbCheck = cursor.fetchone()
        
        if not dbCheck:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName}")
            conn.commit()
            
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='4303', db=dbName, charset='utf8')
        cursor = conn.cursor()
        
        return conn, cursor
    
    except Exception as e:
        connectLogger.error(f'[CONNECT ERROR] => [{e}]')
        
        return None, None

def create_table(dbName, tableName, colsDict):
    create_folder('./log')
    createLogger = logger('create_table', './log/create_table.log')
    conn, cursor = connect_db(dbName)
    try:
        cursor.execute(f"SHOW TABLES LIKE '{tableName}'")
        tableCheck = cursor.fetchone()
        
        if not tableCheck:
            tableSchemas = ', '.join([f"{col} {colType}" for col, colType in colsDict.items()])
            query = f"""
                CREATE TABLE {tableName} (
                    {tableSchemas}
                )
            """
            cursor.execute(query)
            conn.commit()
            createLogger.info(f'[CREATE TABLE] => [{tableName}]')
        else:
            createLogger.info(f'[EXISTED TABLE] => [{tableName}]')
    
    except Exception as e:
        createLogger.error(f"[CREATE ERROR] => [{e}]")
    
    finally:
        cursor.close()
        conn.close()
        
def set_pk(dbName, tableName, colName, constName):
    create_folder('./log')
    setPkLogger = logger('set_pk', './log/set_pk.log')
    conn, cursor = connect_db(dbName)
    try:
        query = f"""
            ALTER TABLE {tableName}
            ADD CONSTRAINT {constName} PRIMARY KEY ({colName})
        """
        cursor.execute(query)
        conn.commit()
        setPkLogger.info(f'[SET PK] => [{tableName} - {colName}]')
        
    except Exception as e:
        setPkLogger.error(f'[PK ERROR] => [{e}]')
    
    finally:
        cursor.close()
        conn.close()
    
def set_fk(dbName, fkTable, pkTable, fkCol, pkCol, constName):
    create_folder('./log')
    setFkLogger = logger('set_fk', './log/set_fk.log')
    conn, cursor = connect_db(dbName)
    try:
        query = f"""
            ALTER TABLE {fkTable}
            ADD CONSTRAINT {constName} FOREIGN KEY ({fkCol}) REFERENCES {pkTable} ({pkCol})
        """
        cursor.execute(query)
        conn.commit()
        setFkLogger.info(f'[SEK FK] => [{fkTable} - {fkCol} Referenced By {pkTable} - {pkCol}]')
        
    except Exception as e:
        setFkLogger.error(f'[FK ERROR] => [{e}]')
        
    finally:
        cursor.close()
        conn.close()
 
def distinct_table(dbName, tableName, colsList):
    create_folder('./log')
    distinctLogger = logger('distinct_table', './log/distinct_table.log')
    conn, cursor = connect_db(dbName)
    try:
        query = f"""
            SELECT COUNT(*) FROM {tableName};
        """
        cursor.execute(query)
        beforeDistinct = cursor.fetchone()[0]
        
        tempSelectSchemas = ', '.join([f'MIN({col}) AS {col}' for col in colsList])
        tempGroupSchemas = ', '.join([f'{col}' for col in colsList])
        query = f"""
            CREATE TEMPORARY TABLE tbl_temp AS
            SELECT {tempSelectSchemas}
            FROM {tableName}
            GROUP BY {tempGroupSchemas};
        """
        distinctLogger.info('[CREATE TEMP TABLE] => [Processing...]')
        cursor.execute(query)
        distinctLogger.info('[CREATE TEMP TALBE] => [Complete]')
        
        distinctSchemas = ' AND '.join([f'tbl_temp.{col} = {tableName}.{col}' for col in colsList])
        query = f"""
            DELETE FROM {tableName}
            WHERE NOT EXISTS (
                SELECT 1 FROM tbl_temp
                WHERE {distinctSchemas}
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
        
        distinctLogger.info(f'[DISTINCT DATA] => Removed : [{removeRows}] \t Remaining : [{afterDistinct}]')
        
    except Exception as e:
        distinctLogger.error(f'[DISTINCT ERROR] => [{e}]')
        
    finally:
        cursor.close()
        conn.close()
        
def insert_data(conn, cursor, tableName, dataList, colsList):
    create_folder('./log')
    insertLogger = logger('insert_data', './log/insert_data.log')
    try:
        insertSchemas = ', '.join([f'{col}' for col in colsList])
        placeHolders = ', '.join(["%s"] * len(colsList))
        query = f"""
            INSERT INTO {tableName} ({insertSchemas})
            VALUES ({placeHolders})
        """
        cursor.executemany(query, dataList)
        conn.commit()
        # insertLogger.info(f'[INSERT DATA] => [Successfully Inserted]')
        
    except Exception as e:
        insertLogger.error(f"[INSERT ERROR] : [{e}]")

def import_data(dbName, tableName, limit):
    create_folder('./log')
    importLogger = logger('import_data', './log/import_data.log')
    conn, cursor = connect_db(dbName)
    try:
        query = f"""
            SELECT * FROM {tableName} LIMIT {limit}
        """
        cursor.execute(query)
        data = cursor.fetchall()
        dataLength = len(data)
        
        importLogger.info(f'[{dataLength}] Row(s) Returned')
        
        return data
        
    except Exception as e:
        importLogger.error(f'[IMPORT ERROR] => [{e}]')
        
        return None
    
    finally:
        cursor.close()
        conn.close()
        
def join_table(dbName, query):
    create_folder('./log')
    joinLogger = logger('join_table', './log/join_table.log')
    conn, cursor = connect_db(dbName)
    try:
        query = query
        cursor.execute(query)
        data = cursor.fetchall()
        
        joinLogger.info(f'[JOIN TABLE] => [Succesfully Join Table]')
        
        return data
        
    except Exception as e:
        joinLogger.error(f'[JOIN ERROR] => [{e}]')
        
        return None
        
    finally:
        cursor.close()
        conn.close()
        
# Code Refactoring => Normalization / Class화
# Query 성능 Update
# DB 설계 다시(ERD / Schema 구조)