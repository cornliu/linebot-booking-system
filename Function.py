#這個檔案的作用是：建立功能列表

#===============這些是LINE提供的功能套組，先用import叫出來=============
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import Globals
import app
import time
#===============LINEAPI=============================================


def localtimetostr(local_time):
    return str(local_time[0])+"/"+str(local_time[1])+"/"+str(local_time[2])

def date_compensate(local_time):
    today = localtimetostr(local_time)
    col = app.sheet.col_values(1)
    ori_length = len(col)
    if today in col:
        pos = col.index(today)
        if (ori_length-pos-1)<7:
            for i in range(7-(ori_length-pos-1)):
                col.append(next_day(col[-1]))
        for i in range(7-(ori_length-pos-1)):
            app.sheet.update_cell(ori_length+1+i,1,col[ori_length+i])

def find_available(date, how_long): #給一個str_date和多久時間，找出可以的時間
    counter = 0
    column = 2
    available_time_list = []
    col = app.sheet.col_values(1)
    if date in col:
        pos = col.index(date)
        row = app.sheet.row_values(pos+1)
        row.extend([""]*(15-len(row)))
        print(row)
        for i in range(1,15):
            if row[i] == "":
                counter+=1
            elif row[i] != "":
                counter = 0
            if counter >= how_long:
                available_time_list.append(i+8-how_long)
    return available_time_list

def if_leap_year(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return 1
            else:
                return 0
        else:
            return 1
    else:
        return 0

def splitdatetoint(date):  #input a date string and return three int
    datelist = date.split("/")
    year = int(datelist[0])
    month = int(datelist[1])
    day = int(datelist[2])
    return int(datelist[0]), int(datelist[1]), int(datelist[2])

def next_day(date):  #input str output str
    datelist = date.split("/")
    year = int(datelist[0])
    month = int(datelist[1])
    day = int(datelist[2])
    #justify whether leao_year or not    
    leap_year = if_leap_year(year)
    max_days = 0
    max_month = 12
    # how many days in this month
    if month in [1, 3, 5, 7, 8, 10, 12]:
        max_days = 31
    elif month in [4, 6, 9, 11]:
        max_days = 30
    else:
        if leap_year:
            max_days = 29
        else:
            max_days = 28
    #counting
    if day+1 > max_days:
        if month+1 > max_month:
            return str(year+1)+"/1"+"/1"
        else:
            return str(year)+"/"+str(month+1)+"/1"
    else:
        return str(year)+"/"+str(month)+"/"+str(day+1)


