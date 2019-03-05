#! /bin/python3
from socket import *
import os

# default params
serverAddr = ("", 50001)

import sys
def usage():
    print("usage: %s [--serverPort <port>]"  % sys.argv[0])
    sys.exit(1)

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--serverPort":
            serverAddr = ("", int(args[0])); del args[0]
        else:
            print("unexpected parameter %s" % args[0])
            usage();
except:
    usage()

print("binding datagram socket to %s" % repr(serverAddr))

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddr)
print("Ready to work!")
directory = (os.getcwd() + '/serverfiles')
segment = {}
serverSocket.settimeout(10)
acknowledged = False

while 1:
    file, clientAddrPort = serverSocket.recvfrom(2048)
    print("from %s: rec'd '%s'" % (repr(clientAddrPort), file)) #debug tool
    print("Looking for file...")
    if not os.path.exists(("%s/%s")%(directory, file.decode())):
        errorMessage = "File not found"
        serverSocket.sendto(errorMessage.encode(), clientAddrPort)
        print(errorMessage)
        pass
    else:
        os.chdir(directory)
        print(file.decode())
        foundFile = open(file.decode(), "r") #open file to read
        data = foundFile.read().replace('\n', ' ')
        # content = foundFile.read(100) #get 100 bytes at a time
        serverSocket.sendto(data.encode(), clientAddrPort)
        while not acknowledged:
            try:
                ACK, address = serverSocket.recvfrom(1024)
                acknowledged = True
            except socket.timeout:
                msg = "Connection lost"
                serversocket.sendto(msg.encode(), clientAddrPort)
        pass
    # modifiedMessage = message.upper()
    # serverSocket.sendto(modifiedMessage, clientAddrPort)
