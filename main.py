from data.data_crawler import *


def main():
    create_folder('./log')
    logging.basicConfig(filename='./log/data_insert.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    crawler(2018, 2023)

if __name__ == '__main__':
    main()