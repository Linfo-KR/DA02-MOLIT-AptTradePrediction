import os
import datetime
import logging


def create_folder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print(f'[ERROR] => Creating Folder Error {dir}')
        
def date_generator(startYear, endYear):
    startDate = datetime.date(startYear, 1, 1)
    endDate = datetime.date(endYear, 12, 31)
    
    dateList = []
    
    currentDate = startDate
    
    while currentDate <= endDate:
        dateList.append(currentDate.strftime('%Y%m'))
        currentDate = currentDate.replace(day=1) + datetime.timedelta(days=32)
        currentDate = currentDate.replace(day=1)
         
    return dateList

def logger(loggerName, logFile, level=logging.INFO):
    logger = logging.getLogger(loggerName)
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    fileHandler = logging.FileHandler(logFile)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    
    return logger