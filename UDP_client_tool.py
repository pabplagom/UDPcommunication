"""
Simple (and really bad) script to connect to a server using UDP.
It is possible to send and receive information using select and socket library

"""


import socket
import select
import sys
import time

#Simple function to write a log file (UDP_log.txt must be created in the same folder)
def write2log(data):
    with open("UDP_log.txt",'a') as udplog:
        udplog.write(time.ctime(time.time()) + ": " + data + "\n")

#Timeout for select
listen_timeout = float(2)

print("UDP Client Tool")
ip_address = input("Insert IP address of the server: ")
udp_port = int(input("Insert UDP port to be used: "))

#Check if the IP is valid
try:
    socket.inet_aton(ip_address)
except socket.error:
    print("ERROR: The IP is not valid! ")
    sys.exit(0)

#Get hostname and IP of the local machine    
hostname = socket.gethostname()
hostname_ip = socket.gethostbyname(hostname)

#FUTURE STEPS: include procedure to check both devices are in the same network

#For the time being, use manual comprobation of the subnetwork domain
print("Please check your IP configuration is in the same network of UDP server:")
print("UDP Server IP: ",ip_address)
print("Local IP: ",hostname_ip)

#Create and bind the socket
UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPsock.bind((hostname_ip,udp_port))
UDPsock.setblocking(0) #to prevent receive function blocking the script


while True:
    
    try:
        readylisten, readywrite, exceptions = select.select([UDPsock],[UDPsock],[],listen_timeout)

        #Go through the lists to check if there is something to read or write
        for s in readylisten:
            if s==UDPsock:
                data = UDPsock.recv(4096)
                datastr = str(data)
                print("<<", datastr[2:-1])
                write2log(datastr[2:-1])
        for s in readywrite:
            if s==UDPsock:
                MESSAGE = input(">> ")
                UDPsock.sendto(bytes(MESSAGE,'utf-8'),(ip_address,udp_port))
                write2log(MESSAGE)
    except (KeyboardInterrupt, SystemExit):
        print("Closing the connection!...")
        UDPsock.close()
        print("Closing UDP Client Tool")
        sys.exit(0)
