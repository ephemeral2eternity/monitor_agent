#!/usr/bin/python
import socket
import time
import re
import sys
from subprocess import Popen, PIPE

def traceroute(host):
    hops = dict()
    if sys.platform == 'win32':
        cmd = ['tracert', host]
    else:
        cmd = ['traceroute', host]
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

            if sys.platform == 'win32':
                hop['Addr'] = tr_data[-1]
                tr_data.pop()
                tr_data.pop(0)
            else:
                hop['Addr'] = tr_data[1]
                tr_data.pop(1)
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
                hop['Time'] = 5000
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
    hops = traceroute('130.211.180.109')
    print hops
