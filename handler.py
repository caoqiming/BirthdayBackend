# coding=utf-8
import pymysql.cursors
import lunar
import re

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

def add_user_handler(post_dict):
    data = {'message' : 'ok'}
    if 'username' not in post_dict:
        data['message']="miss username"
        return data
    if 'password' not in post_dict:
        data['message']="miss password"
        return data
    if 'email' not in post_dict:
        data['message']="miss email"
        return data
    #检查是否已经有该用户
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='websideuser', password='ajey', db='websideuser', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = '%s\'%s\''%('SELECT password FROM usertable where username=',post_dict['username'])
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()  
    connection.close()

    if(len(result)!=0):
        data['message']="username already existed"
        return data
    
    #添加用户
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='websideuser', password='ajey', db='websideuser', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = 'INSERT INTO usertable (username,password,email) VALUES (\'%s\',\'%s\',\'%s\')'%(post_dict['username'] , post_dict['password'], post_dict['email'])
    try:
        cursor.execute(sql)
        connection.commit()
        result = cursor.fetchall()
        connection.close()
    except:
        data['message']="error" 
        data['extra']="INSERT INTO usertable failed"
        return data


    #为用户添加生日表
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='ylbirthday', password='shengrikuaile', db='birthday', 
                                charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = '''CREATE TABLE `%s` (
            `name` varchar(128) NOT NULL,
            `year` int(11) DEFAULT NULL,
            `month` int(11) DEFAULT NULL,
            `day` int(11) DEFAULT NULL,
            PRIMARY KEY (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8'''%(post_dict['username'])
    try:
        cursor.execute(sql)
        connection.commit()
        result = cursor.fetchall()
        connection.close()
    except:
        data['message']="error" #可能是该表已经存在
        data['extra']="CREATE TABLE failed"
        return data

    return data

def delete_user_handler(post_dict):
    data = {'message' : 'ok'}
    if 'username' not in post_dict:
        data['message']="miss username"
        return data
    if 'superkey' not in post_dict:
        data['message']="only cqm can use this"
        return data
    if post_dict['superkey'] != 'AjeyForever':
        data['message']="only cqm can use this"
        return data

    #删除用户
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='websideuser', password='ajey', db='websideuser', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = '%s\'%s\''%('DELETE FROM usertable WHERE username=',post_dict['username'])
    try:
        cursor.execute(sql)
        connection.commit()
        result = cursor.fetchall()
        connection.close()
    except:
        data['message']="error" 
        data['extra'] ="delete from usertable failed"
        return data

    #删除用户的生日表
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='ylbirthday', password='shengrikuaile', db='birthday', 
                                charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = 'DROP TABLE %s'%(post_dict['username'])
    try:
        cursor.execute(sql)
        connection.commit()
        result = cursor.fetchall()
        connection.close()
    except:
        data['message']="error" 
        data['extra'] ="DROP TABLE failed"
        return data

    return data

def judge_phone(tel):
    tel = str(tel)
    ret = re.match(r"^1[35789]\d{9}$", tel)
    if ret:
        return True
    else:
        return False

def set_tel_handler(post_dict): #设定电话号码
    data = {'message' : 'ok'}
    if 'username' not in post_dict:
        data['message']="miss username"
        return data
    if 'password' not in post_dict:
        data['message']="miss password"
        return data
    if 'tel' not in post_dict:
        data['message']="miss tel"
        return data
    if not judge_phone(post_dict['tel']):
        data['message']="invalid tel"
        return data
    #先检查账号密码
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

    connection = pymysql.connect(host='127.0.0.1', port=3306, user='websideuser', password='ajey', db='websideuser', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = 'UPDATE usertable SET tel=%s WHERE username=\'%s\'' % (post_dict['tel'],post_dict['username'])
    try:
        cursor.execute(sql)
        connection.commit()
        result = cursor.fetchall()
        connection.close()
    except:
        data['message']="error"
        data['extra']="UPDATE usertable failed"

    return data

def clear_tel_handler(post_dict): #清除电话号码
    data = {'message' : 'ok'}
    if 'username' not in post_dict:
        data['message']="miss username"
        return data
    if 'password' not in post_dict:
        data['message']="miss password"
        return data
    #先检查账号密码
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

    connection = pymysql.connect(host='127.0.0.1', port=3306, user='websideuser', password='ajey', db='websideuser', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = 'UPDATE usertable SET tel=NULL WHERE username=\'%s\'' % (post_dict['username'])
    try:
        cursor.execute(sql)
        connection.commit()
        result = cursor.fetchall()
        connection.close()
    except:
        data['message']="error"
        data['extra']="UPDATE usertable failed"

    return data












    