## python udpserver.py <udp_port>
## run as: python udpserver.py  12345
##
## send sample UDP packet.
##
## echo -n "hello" > /dev/udp/127.0.0.1/12345

import logging
import socket
import sys
import os
import datetime

# Setup logging.
log = logging.getLogger("temp_server")
format_cons = "%(asctime)s %(name)-12s %(levelname)8s\t%(message)s"
logging.basicConfig(level = logging.DEBUG, format = format_cons)

# Global variables.
server_port = int(sys.argv[1])

def udp_server(host = "0.0.0.0", port = server_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    log.info("Listening on 'udp/%s:%s'..." % (host, port))
    
    s.bind((host, port))
    while True:
        # 16-byte buffer is enough for my needs.
        (data, addr) = s.recvfrom(32)
        yield data

for data in udp_server():   
    log.debug("Received data %r." % (data))
    
    tokns = data.decode("ascii").split(";")
    formatted_data = "influx -database 'home_data' -execute 'INSERT sensors,sensor_id={} temp={},humidity={}'".format(tokns[0], tokns[1], tokns[2])

    print(formatted_data)
    os.system(formatted_data)