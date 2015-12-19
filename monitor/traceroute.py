#!/usr/bin/python
import socket
import time
import re
import sys
from subprocess import Popen, PIPE

def findAddr(tr_data):
    item_ind = 0
    for item in tr_data:
        if len(item.split('.')) > 3:
            return item_ind, item
        item_ind += 1

    return -1, '*'

def traceroute(host):
    hops = dict()
    if sys.platform == 'win32':
        cmd = ['tracert', host]
    else:
        cmd = ['traceroute', '-I', host]
    p = Popen(cmd, stdout=PIPE)
    while True:
        line = p.stdout.readline()
        if not line:
            break

        tr_line = line.replace('ms', '')
        if sys.platform == 'win32':
            tr_line = re.sub(r'\[.*?\]', '', tr_line)
        else:
            tr_line = re.sub(r'\(.*?\)', '', tr_line)
        tr_data = tr_line.split()

        if len(tr_data) < 1:
            continue

        if tr_data[0].isdigit():
            hop_id = int(tr_data[0])
            hop = {}
            addr_ind, addr = findAddr(tr_data)

            hop['Addr'] = addr
            if addr_ind > 0:
                tr_data.pop(addr_ind)
            tr_data.pop(0)

            hop_time_exist = False
            total_hop_time = 0
            probe_times = 0
            for tr_item in tr_data:
                if tr_item.isdigit():
                    total_hop_time += float(tr_item)
                    probe_times += 1
                    hop_time_exist = True
                elif '<' in tr_item:
                    total_hop_time += 1
                    probe_times += 1
                    hop_time_exist = True

            if hop_time_exist:
                hop['Time'] = total_hop_time / float(probe_times)
            else:
                hop['Time'] = '*'
            print hop
            hops[hop_id] = hop

    return hops

def trVMs(vmList):
    srvHops = {}
    srvNames = vmList.keys()
    for srv in srvNames:
        hops = traceroute(vmList[srv]['ip'])
        srvHops[srv] = hops
    return srvHops

if __name__ == "__main__":
    hops = traceroute('216.239.47.121')
    print hops
