#!/usr/bin/python

import socket
import threading
import select
import time
import argparse

def main():

    class Chat_Server(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
                self.conn = None
                self.addr = None
            def run(self):
                HOST = ''
                PORT = int(port_number)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST,PORT))
                s.listen(1)
                self.conn, self.addr = s.accept()
                # Select loop for listen
                while self.running == True:
                    inputready,outputready,exceptready = select.select ([self.conn],[self.conn],[])
                    for input_item in inputready:
                        # Handle sockets
                        data = self.conn.recv(1024)
                        if data:
                            print ("\033[1;31;47m > " + data + "\033[0m")
                        else:
                            break
                    time.sleep(0)
            def kill(self):
                self.running = 0
     
    class Chat_Client(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.host = None
                self.sock = None
                self.running = 1
            def run(self):
                PORT = int(port_number)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, PORT))
                # Select loop for listen
                while self.running == True:
                    inputready,outputready,exceptready = select.select ([self.sock],[self.sock],[])
                    for input_item in inputready:
                        # Handle sockets
                        data = self.sock.recv(1024)
                        if data:
                            print ("\033[1;31;47m > " + data + "\033[0m")
                        else:
                            break
                    time.sleep(0)
            def kill(self):
                self.running = 0
                
    class Text_Input(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
            def run(self):
                while self.running == True:
                  text = raw_input('')
                  try:
                      chat_client.sock.sendall(text)
                  except:
                      Exception
                  try:
                      chat_server.conn.sendall(text)
                  except:
                      Exception
                  time.sleep(0)
            def kill(self):
                self.running = 0

    # prompt and parse the command line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('type', help='Enter Server or Client')
    arg_parser.add_argument('port', help='Enter Port Number to Use')
    arg_parser.add_argument('--version','-v', action='version', version='%(prog)s 1.0')
    results = arg_parser.parse_args()

    type_connection = results.type
    port_number = results.port
    chat_server = Chat_Server()
    chat_client = Chat_Client()

    if type_connection.lower() == ('server'):
        print "Server Mode Selected"
        print "Using port: ", port_number
        chat_server.start()
    elif type_connection == ('client'):
        print "Client Mode selected"
        print "Using port: ", port_number
        ip_addr = raw_input('Please Enter the IP of the Server: ')
        print "Connecting to: ", ip_addr
        chat_client.host = ip_addr
        chat_client.start()
    else:
        print "You must select SERVER or CLIENT"
        print "Exiting program"
        print ""
        exit()

    text_input = Text_Input()
    text_input.start()


if __name__ == "__main__":
    main()
