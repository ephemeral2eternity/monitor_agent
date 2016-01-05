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
# cdn_host = "40.122.125.188"
# cdn_host = "aws.cmu-agens.com"
hop_data_folder = os.getcwd() + '/hopData/'

hops = traceroute(cdn_host)
print hops

hop_ids = sorted(hops.keys(), key=int)
for hop_id in hop_ids:
    cur_hop_ip = hops[hop_id]['IP']
    if cur_hop_ip is '*':
        continue

    if not is_reserved(cur_hop_ip):
        hop_info = ipinfo(cur_hop_ip)
        save_ipinfo(hop_data_folder, hop_info)
        print hop_info