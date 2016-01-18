#  coding: utf-8 
import SocketServer
import os
import mimetypes

# Copyright 2016 Abram Hindle, Eddie Antonio Santos, Falon Scheers
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


class MyWebServer(SocketServer.BaseRequestHandler):

    Output_msgs = {200: "HTTP/1.1 200 OK \r\n", 
                   404: "HTTP/1.1 404 Not Found \n\n Page not found! or not? Who knows really...", 
                   405: "HTTP/1.1 405 Method Not Allowed \r\n", 
                   400: "HTTP/1.1 400 Bad Request \r\n BAD REQUEST!! Try something better!"} 

    def handle(self):
        ''' first item in request is type of request, check for 'GET'
            The path of the item is the second data item written
            Check if in the servable location and send to print correct code
        '''
        # setup, parse and check for bad requests
        self.data = self.request.recv(1024).strip().split(" ")
        if self.data[0] != "GET":
            self.send_back(405)
        if len(self.data) > 1:
            self.item_path = self.data[1]
        else:
            self.send_back(400)

        # if not in the /www folder we don't want to serve it
        needed = os.path.abspath("./www") 
        self.item_path = "./www" + self.item_path
        if self.item_path[-1] == "/" or os.path.isdir(self.item_path):
            self.item_path += "/index.html"
        try:
            if needed[0:] != os.path.abspath(self.item_path)[0:len(needed)]:
                self.send_back(404)
            else: 
                self.send_back(200)
        except IOError:
            self.send_back(404)

    # fetch content from valid pages or print error codes and message
    def send_back(self, code):
        if code == 200:
            file = open(os.path.abspath(self.item_path), 'r')
            content = file.read()
            mime_type = "Content-Type: " + mimetypes.guess_type(self.item_path)[0] + "\r\n"
            content_length = "Content-Length: " + str(len(content)) + "\r\n"
            to_send = self.Output_msgs[code] + mime_type + content_length + "\n" + content
            file.close()
        else:
            to_send = self.Output_msgs[code]
        self.request.sendall(to_send)
        return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
