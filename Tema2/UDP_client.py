import socket
import logging
import time
import threading
from sets import Set

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 10000
adresa = '172.111.0.14'
server_address = (adresa, port)

n = 10000
window_size = 10
first_value = 1
send_timeout = .1
buffsize = 4096
receive_check_interval = .00001
confirmed_set = Set([])


def receive():
    global first_value

    while True:
        data, address = sock.recvfrom(buffsize)
        logging.info('Receiving %s', data)
        if (not (data in confirmed_set)) and int(data) >= first_value and int(data) < first_value + window_size:
            confirmed_set.add(data)


def update():
    global first_value
    while True:
        while str(first_value) in confirmed_set:
            confirmed_set.remove(str(first_value))
            first_value = first_value + 1


t_receive = threading.Timer(0, receive)
t_receive.start()

t_update = threading.Timer(0, update)
t_update.start()

while True:
    crt_first_value = first_value
    for i in range(window_size):
        int_mesaj = i + crt_first_value
        if int_mesaj > n:
            break
        mesaj = str(int_mesaj)
        if mesaj in confirmed_set:
            continue
        logging.info('Sending %s', mesaj)
        time.sleep(send_timeout)
        sent = sock.sendto(mesaj, server_address)

    if first_value > n:
        logging.info("Job's done")
        t_receive.stop()
        t_update.stop()
        sock.close()
        break
