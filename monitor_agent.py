## Testing the CDN client in a VoD System
# test_cdn_client.py
# Chen Wang, Oct. 23, 2015
# chenw@cmu.edu
import random
import sys
import os
import logging
import shutil
import time
from datetime import datetime
from utils import *
from monitor.ping import *
from monitor.traceroute import *
from monitor.load_vms import *

### Get client name and attache to the closest cache agent
agent_name = getMyName()

## Denote the server info
srvs = load_vms()

### Get the server to start streaming
cur_ts = time.time()

## ping all servers
ping_file_name = 'ping@' + agent_name + '@' + str(int(cur_ts))
srvPINGs = pingVMs(srvs)
selectedSrv = srvs[min(srvPINGs, key=lambda k: srvPINGs[k])]['ip']
writeJson(ping_file_name, srvPINGs)

cur_ts = time.time()
## Traceroute all srvs
tr_file_name = 'tr@' + agent_name + '@' + str(int(cur_ts))
srvHops = trVMs(srvs)
writeJson(tr_file_name, srvHops)
