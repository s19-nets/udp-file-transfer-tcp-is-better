#! /bin/python3
from socket import *
import os

# default params
serverAddr = ('localhost', 50000)

import sys, re

def usage():
    print("usage: %s [--serverAddr host:port]"  % sys.argv[0])
    sys.exit(1)

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--serverAddr":
            addr, port = re.split(":", args[0]); del args[0]
            serverAddr = (addr, int(port))
        else:
            print("unexpected parameter %s" % args[0])
            usage();
except:
    usage()


clientSocket = socket(AF_INET, SOCK_DGRAM)
requestFile = input("File to get from server:")
clientSocket.sendto(requestFile.encode(), serverAddr)
reply = "ACK"
end = True

fileName, serverAddrPort = clientSocket.recvfrom(2048)
path = (os.getcwd() +'/'+ requestFile)
out_file = open(path, "wb+") #[w]rite as [b]inary
out_file.write(fileName)
out_file.close()
# framedSend(sock, payload, 1)

# while not end: #add condition
#      modifiedMessage, serverAddrPort = clientSocket.recvfrom(2048)
#      print(modifiedMessage.decode())
#      if modifiedMessage:
#          clientSocket.sendto(reply.encode(), serverAddr)
#          pass
# pass
