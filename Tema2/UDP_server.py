import socket
import logging
import threading
from sets import Set

logging.basicConfig(format=u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 10000
address = '172.111.0.14'
server_address = (address, port)
sock.bind(server_address)
logging.info("Server is started on %s and port %d", address, port)

first_value = 1
n = 10000
buffsize = 4096
window_size = 10
received_set = Set([])

def update():
    global first_value
    while True:
        while str(first_value) in received_set:
            received_set.remove(str(first_value))
            first_value = first_value + 1

t_update = threading.Timer(0, update)
t_update.start()

while True:
    data, address = sock.recvfrom(buffsize)
    logging.info('Received %s', data)

    if data:
        if int(data) < first_value + window_size:
            logging.info('Sending %s', data)
            sent = sock.sendto(data, address)
        if (not (data in received_set)) and int(data) >= first_value and int(data) < first_value + window_size:
            received_set.add(data)

    if first_value > n:
        logging.info("Job's done")
        t_update.stop()
        sock.close()
        break
