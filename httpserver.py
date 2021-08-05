from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi
 
message1 = {'message': 'jojo, please use post instead of get'}
message2 = {'message': 'miss the parameter: type'}
message3 = {'message': 'request is not json'}
host = ('localhost', 8888)

def login_handler(post_dict):
    data = {'message' : 'ok'}
    if 'username' not in post_dict:
        data['message']="miss username"
    if 'password' not in post_dict:
        data['message']="miss password"
    return data



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
            post_dict=json.loads(post_body)
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


        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
 
if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()