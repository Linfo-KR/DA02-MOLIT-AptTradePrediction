from data.data_crawler import *
from data.sql_db import *


def main():
    logging.basicConfig(filename='./log/data_insert.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    

if __name__ == '__main__':
    main()