# coding=utf-8
from http.server import HTTPServer, BaseHTTPRequestHandler
from handler import *
import json
import cgi
 
message1 = {'message': 'jojo, please use post instead of get'}
message2 = {'message': 'miss the parameter: type'}
message3 = {'message': 'request is not json'}
host = ('0.0.0.0', 8888)




class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(message1).encode())
 
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        try:
            #print(post_body.decode())
            post_dict=json.loads(post_body.decode())
        except:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(message3).encode())
            return

        print(post_dict)
        if 'type' not in post_dict:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(message2).encode())
            return
        if post_dict['type']=='login':
            data=login_handler(post_dict)
        elif post_dict['type']=='query': #查询生日数据
            data=query_birthday_handler(post_dict)
        elif post_dict['type']=='insert': #插入生日数据
            data=insert_handler(post_dict)
        elif post_dict['type']=='delete': #删除生日数据
            data=delete_birthday_handler(post_dict)
        elif post_dict['type']=='add_user': #添加用户
            data=add_user_handler(post_dict)
        elif post_dict['type']=='delete_user': #删除用户，仅自用
            data=delete_user_handler(post_dict)
        elif post_dict['type']=='set_tel': #设置电话号码
            data=set_tel_handler(post_dict)
        elif post_dict['type']=='clear_tel': #删除电话号码
            data=clear_tel_handler(post_dict)
            
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
 
if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()