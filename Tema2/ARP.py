from scapy.all import *

pdst = '198.13.13.0/16'
eth = Ether(dst='ff:ff:ff:ff:ff:ff')
arp = ARP(pdst=pdst) #Destination ip
ans, unans = srp(eth/arp, timeout=1)

for pkt in ans:
   print(pkt[1].psrc, '---', pkt[1].hwsrc)
