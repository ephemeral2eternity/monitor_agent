import json
import requests
import os
from host2ip import *

def ipinfo(ip):
    url = 'http://ipinfo.io/' + ip
    resp = requests.get(url)
    hop_info = json.loads(resp.text)
    hop_org = hop_info['org']
    hop_org_items = hop_org.split()
    hop_info['AS'] = hop_org_items[0]
    hop_info['ISP'] = " ".join(hop_org_items[1:])
    return hop_info

def save_ipinfo(outPath, hop_info):
    try:
        os.stat(outPath)
    except:
        os.mkdir(outPath)

    cur_ip = hop_info['ip']
    out_file = outPath + cur_ip + '.json'
    if not os.path.exists(out_file):
        with open(out_file, 'w') as outfile:
            json.dump(hop_info, outfile, sort_keys = True, indent = 4, ensure_ascii=False)


if __name__ == "__main__":
    hop_name = "et-5-0-0.120.rtr.eqny.net.internet2.edu"
    if is_hostname(hop_name):
        ip = host2ip(hop_name)
    else:
        ip = hop_name

    hop_info = ipinfo(ip)
    outPath = 'D://GitHub/monitor_agent/hopData/'
    save_ipinfo(outPath, hop_info)