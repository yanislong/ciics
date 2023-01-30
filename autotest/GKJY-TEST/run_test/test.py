#!/usr/bin/env python3

from Crypto.Hash import MD4
import requests
import sys
sys.path.append('/root/lhl/myPerformance/GKJY-TEST/')
import config
import base64

aa = base64.b64encode(config.mm("TElaT05HV1U=59b0799" + '12345678').encode("utf-8"))
print(len(aa))
print(len("R/rVVqz7tPVPHtw7b2GUBq6hAqM="))

obj = MD4.new()
obj.update(b'1234567')
print(obj.hexdigest())

mimahash = "R/rVVqz7tPVPHtw7b2GUBq6hAqM="
salt = "TElaT05HV1U=59b0799"
