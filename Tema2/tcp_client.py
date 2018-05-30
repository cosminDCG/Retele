
from scapy.all import *
import sys

dst = '198.13.0.14'
dport = '8080'

seq = 12345

synack = sr1(IP(dst=dst)/TCP(dport=dport, flags='S', seq=seq))
send(IP(dst=dst)/TCP(dport=dport, flags='A', seq=synack.ack, ack=synack.seq+1), count=1)

seq = synack.ack
ack = synack.seq + 1

ip = IP()
ip.dst=dst
ip.tos=int('011110' + '11', 2)

optiune = 'MSS'
op_index = TCPOptions[1][optiune]
op_format = TCPOptions[0][op_index]
valoare = struct.pack(op_format[1], 2)


for i in 'ret':
    send(ip/TCP(dport=dport, flags='PACE', seq=seq, ack=ack, options = [(optiune, valoare)])/i)
    seq = seq + 1
    ans, unans = sniff(filter='tcp and host ' + dst, count=2)
    pkt = ans[0]
    ack = pkt.seq + len(pkt[Raw])

try:
	data = sr1(ip/TCP(dport=dport, flags='PACE', seq=seq, ack=ack,options = [(optiune, valoare)])/'ele')
	seq += 3

	send(ip/TCP(dport=dport, flags='R', seq=seq, ack=ack))
finally:
	logging.info('some logs')

