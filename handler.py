# coding=utf-8
import pymysql.cursors

def login_handler(post_dict):
    data = {'message' : 'ok'}
    if 'username' not in post_dict:
        data['message']="miss username"
        return data
    if 'password' not in post_dict:
        data['message']="miss password"
        return data

    connection = pymysql.connect(host='127.0.0.1', port=3306, user='websideuser', password='ajey', db='websideuser', 
                                charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = '%s\'%s\''%('SELECT password FROM usertable where username=',post_dict['username'])
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()
    connection.close()

    if(len(result)!=1):
        data['message']="user not found or user name error"
        return data
    if(result[0]['password']!=post_dict['password']):
        data['message']="password error"
        return data
    return data
