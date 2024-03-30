import os
import datetime


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