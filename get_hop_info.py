## Do Traceroute to a CDN host and gets detailed info on each hop.
# test_cdn_client.py
# Chen Wang, Oct. 23, 2015
# chenw@cmu.edu
from utils import *
from monitor.traceroute import *
from ipinfo.host2ip import *
from ipinfo.ipinfo import *

### Get client name and attache to the closest cache agent
agent_name = getMyName()

## Denote the server info
cdn_host = "cmu-agens.azureedge.net"
hop_data_folder = os.getcwd() + '/hopData/'

hops = traceroute(cdn_host)
print hops

hop_ids = sorted(hops.keys(), key=int)
for hop_id in hop_ids:
    cur_hop = hops[hop_id]['Addr']
    if is_hostname(cur_hop):
        cur_hop_ip = host2ip(cur_hop)
    else:
        cur_hop_ip = cur_hop

    hop_info = ipinfo(cur_hop_ip)
    save_ipinfo(hop_data_folder, hop_info)
    print hop_info

