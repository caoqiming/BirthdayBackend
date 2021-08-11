from sxtwl import Lunar
from datetime import datetime
lunar = Lunar()  # 实例化日历库

def solar_lunar(year,month,day):
    day=lunar.getDayBySolar(year, month, day)
    m=day.Lmc
    if m<2:
        m=m+11
    else:
        m=m-1
    return day.Lyear+1984, m, day.Ldi + 1

def lunar_solar(year,month,day,r=False):
    day=lunar.getDayByLunar(year, month, day,r)
    return day.y , day.m , day.d

def days_from_next(data): #距离下个生日还要多少天 可直接输入数据库查询结果
    year_now=datetime.now().year
    month_now=datetime.now().month
    day_now=datetime.now().day
    to_day=datetime(year_now,month_now,day_now)
    ans=[]
    for one in data:
        y,m,d=lunar_solar(year_now,one['month'],one['day']) #先找到阴历生日对应今年的阳历哪一天
        one_day=datetime(y,m,d)
        days2next=(one_day-to_day).days
        if(days2next<0): #如果今年的阴历生日已经过了就算明年的
            y,m,d=lunar_solar(year_now+1,one['month'],one['day']) #那就找到阴历生日对应明年的阳历哪一天
            one_day=datetime(y,m,d)
            days2next=(one_day-to_day).days
        ans.append(days2next)
    return ans



