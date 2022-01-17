import socket
import threading
import sys
import time
from random import randint
class Server:
    connections = []
    peers = []
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("0.0.0.0", 8008))
        sock.listen(1)
        print("Waiting for incoming connections....")
        

        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args = (c,a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            self.peers.append(a[0])
            print(str(a[0]) + ':' + str(a[1]), "connected")
            self.sendPeers()
    def handler(self, c,a):
        global connections
        while True:
            data= c.recv(1024)
            for connection in self.connections:
                connection.send(bytes(data))
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break

    def sendPeers(self):
            p = ""
            for peer in self.peers:
                p = p + peer + ","  
            for connection in self.connections:
                connection.send(b'\x11' + bytes(p, "utf-8"))
class Client:
    def sendMSG(self, sock):
        while True:
            sock.send(bytes(input(""), 'utf-8'))

    def __init__(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((address, 8008))

        inputThread = threading.Thread(target=self.sendMSG, args=(sock,))
        inputThread.daemon = True
        inputThread.start()
        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11':
                self.updatePeers(data[1:])
            else:
                print(str(data,'utf-8'))
            print(str(data,'utf-8'))

    def updatePeers(self, peerData):
        p2p.peers = str(peerData, "utf-8").split(",")[:-1]

class p2p:
    peers = ['127.0.0.1']
while True:
    try:
        print("Trying to connect....")
        time.sleep(randint(1, 5))
        for peer in p2p.peers:
            try:
                client = Client(peer)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
            if randint(1, 20) == 1: 
                try:
                    server = Server()
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    print("Could not start the server")
    except KeyboardInterrupt:
        sys.exit(0)
