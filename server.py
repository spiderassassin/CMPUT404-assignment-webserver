
import socketserver
import os



# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        
        
        self.data = self.request.recv(1024).strip()
        data = self.data.decode("utf-8").split()
        
       
        url = data[1].strip()
        if(url[0] == "/"):
            url = url[1:]
      
        
        
       
        if(data[0] != "GET"):
            print("HTTP/1.1 405 Method Not Allowed\r\n" )
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
            return

           
        path = os.path.join(os.getcwd(), "www", url)
    
        #404
        if((os.path.exists(path) != True) or ("../" in path) ):
            print("HTTP/1.1 404 Not Found\r\n" )
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
            return

        #directory
        if(os.path.isfile(path) == False):
            if ((url != "") and (url[len(url) - 1] != "/")):#301 error
                url = url + "/"
                path = os.path.join(os.getcwd(), "www", url)
                message_301 = "HTTP/1.1 301 Moved Permanently\r\n Location: http://127.0.0.1:8080 " + str(path) + "\r\n"
                self.request.sendall(bytearray(message_301,'utf-8'))
                print(message_301 )

            path = os.path.join(path, "index.html")#add fill to directory

        
        file = open(path, "r")
        content = file.read()
        length = len(content)
        path_string = str(path)
        index = path_string.find('.')
        type = path_string[index + 1:]
        print(type)
        output = "HTTP/1.1 200 OK\r\nContent-Type: text/" + type + "\r\n" + content
        print(output)
        self.request.sendall(bytearray(output,'utf-8'))




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
