# coding=utf-8
import pymysql.cursors
import lunar

def login_handler(post_dict):
    data = {'message' : 'ok'}
    if 'username' not in post_dict:
        data['message']="miss username"
        return data
    if 'password' not in post_dict:
        data['message']="miss password"
        return data

    connection = pymysql.connect(host='127.0.0.1', port=3306, user='websideuser', password='ajey', db='websideuser', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = '%s\'%s\''%('SELECT password FROM usertable where username=',post_dict['username'])
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()  
    connection.close()

    if(len(result)==0):
        data['message']="user name error"
        return data
    if(len(result)>1):
        data['message']="too many users, please inform caoqiming"
        return data
    if(result[0]['password']!=post_dict['password']):
        data['message']="password error"
        return data
    return data


def query_birthday_handler(post_dict):
    data = {'message' : 'ok'}
    if 'username' not in post_dict:
        data['message']="miss username"
        return data
    if 'password' not in post_dict:
        data['message']="miss password"
        return data

    connection = pymysql.connect(host='127.0.0.1', port=3306, user='websideuser', password='ajey', db='websideuser', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = '%s\'%s\''%('SELECT password FROM usertable where username=',post_dict['username'])
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()  
    connection.close()

    if(len(result)==0):
        data['message']="user name error"
        return data
    if(len(result)>1):
        data['message']="too many users, please inform caoqiming"
        return data
    if(result[0]['password']!=post_dict['password']):
        data['message']="password error"
        return data

    #查询生日
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='ylbirthday', password='shengrikuaile', db='birthday', 
                                charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = '%s%s%s'%('SELECT * FROM ' , post_dict['username'] ,' ORDER BY month,day')
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()
    connection.close()
    
    days2next=lunar.days_from_next(result) #下一个生日的日期
    sorted_days2next=sorted(enumerate(days2next), key=lambda x:x[1]) #排序
    index = [x[0] for x in sorted_days2next]
    pesponse=[]
    for one in index:
        temp_dic={}
        temp_dic['name']=result[one]['name']
        temp_dic['y']=result[one]['year']
        temp_dic['m']=result[one]['month']
        temp_dic['d']=result[one]['day']
        temp_dic['next']=days2next[one]
        pesponse.append(temp_dic)
    data['result']=pesponse
    return data

def insert_handler(post_dict): #添加生日
    data = {'message' : 'ok'}
    if 'username' not in post_dict:
        data['message']="miss username"
        return data
    if 'password' not in post_dict:
        data['message']="miss password"
        return data
    if 'name' not in post_dict:
        data['message']="miss name"
        return data
    if 'islunar' not in post_dict: #0表示阳历，其他表示阴历
        data['message']="miss islunar"
        return data
    if 'year' not in post_dict: 
        data['message']="miss year"
        return data
    if 'month' not in post_dict: 
        data['message']="miss month"
        return data
    if 'day' not in post_dict: 
        data['message']="miss day"
        return data

    connection = pymysql.connect(host='127.0.0.1', port=3306, user='websideuser', password='ajey', db='websideuser', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = '%s\'%s\''%('SELECT password FROM usertable WHERE username=',post_dict['username'])
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()  
    connection.close()
    if(len(result)==0):
        data['message']="user name error"
        return data
    if(len(result)>1):
        data['message']="too many users, please inform caoqiming"
        return data
    if(result[0]['password']!=post_dict['password']):
        data['message']="password error"
        return data

    #计算生日
    if post_dict['islunar'] == 0: #阳历，需要换算
        y,m,d = lunar.solar_lunar(post_dict['year'],post_dict['month'],post_dict['day'])
    else:
        y=post_dict['year']
        m=post_dict['month']
        d=post_dict['day']
    #插入生日
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='ylbirthday', password='shengrikuaile', db='birthday', 
                                charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = 'INSERT INTO %s (name,year,month,day) VALUES (\'%s\',%d,%d,%d)'%(post_dict['username'] ,post_dict['name'],y,m,d)
    try:
        cursor.execute(sql)
        connection.commit()
        result = cursor.fetchall()
        connection.close()
    except:
        data['message']="error" #可能是名字已经存在

    return data

def delete_birthday_handler(post_dict): #删除生日
    data = {'message' : 'ok'}
    if 'username' not in post_dict:
        data['message']="miss username"
        return data
    if 'password' not in post_dict:
        data['message']="miss password"
        return data
    if 'name' not in post_dict:
        data['message']="miss name"
        return data
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='websideuser', password='ajey', db='websideuser', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = '%s\'%s\''%('SELECT password FROM usertable where username=',post_dict['username'])
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()  
    connection.close()

    if(len(result)==0):
        data['message']="user name error"
        return data
    if(len(result)>1):
        data['message']="too many users, please inform caoqiming"
        return data
    if(result[0]['password']!=post_dict['password']):
        data['message']="password error"
        return data

    #删除生日
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='ylbirthday', password='shengrikuaile', db='birthday', 
                                charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = 'DELETE FROM %s WHERE name=\'%s\''%(post_dict['username'], post_dict['name'])
    try:
        cursor.execute(sql)
        connection.commit()
        result = cursor.fetchall()
        connection.close()
    except:
        data['message']="error" #可能是要删除的不存在

    return data