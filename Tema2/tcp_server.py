import socket
import logging
import time
import random

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = '8080'
adresa = '0.0.0.0'
server_address = (adresa, port)
sock.bind(server_address)
logging.info("Serverul a pornit pe %s si portnul portul %d", adresa, port)
sock.listen(1)
conexiune, address = sock.accept()
logging.info("Handshake cu %s", address)
while True:
    data = conexiune.recv(1)
    logging.info('Content primit: "%s"', data)
    conexiune.send('f')
conexiune.close()
sock.close()
