#!/usr/bin/env python3

from mosRsa_split import RsaUtil
import requests
import json
import config
import testPram


data = "{\"0\":\"0\",\"1\":\"1\",\"10\":\"10\",\"11\":\"11\",\"12\":\"12\",\"13\":\"13\",\"14\":\"14\",\"15\":\"15\",\"16\":\"16\",\"17\":\"17\",\"18\":\"18\",\"19\":\"19\",\"2\":\"2\",\"3\":\"3\",\"4\":\"4\",\"5\":\"5\",\"6\":\"6\",\"7\":\"7\",\"8\":\"8\",\"9\":\"9\"}"
data = "华" * 540
data = '{"freezePersonalAmount":"2757.00","orderID":"20230411134526761","identitycardCode":"152701197712100618","freezePublicAmount":"0","source":"3","policyCode":"202012140933","freezePersonalAmount2":"3178.42","orgClaimId":"0203-00543-00002","thirdOnlyKey":"20230411134526928"}'
data = '{"orderID":"20230411144426822","trade_id"}'
aaa = "9ZlwofWzeRzJQRc7BAH20230411"
data = '{"unfreeze_reason":"撤销理算","tradeId":"9ZlwofWzeRzJQRc7BAH20230411"}'
#data = '{"tradeId":"TjSqDacLcJBhCgTMPu020230411"," refundId":"","unfreeze_reason":"撤销理算","orgClaimId":"0203-00548-00002","caseId":"1582915165823729666"}'
data = '{"freezePersonalAmount":"2757.00","orderID":"20230411160706405","identitycardCode":"152701197712100618","freezePublicAmount":"0","source":"3","policyCode":"202012140933","freezePersonalAmount2":"5178.42","orgClaimId":"0203-00548-00002","thirdOnlyKey":"20230411164802"}'
pri_key = '''
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAISIBS2VhrtvpqK2QNOMZC3s9Py0ZBY1BayfPNHUtykeTgbJDVa8oNKa9uG1tq8fTmB/3fCVu+yfSW4iJ/O08O+UEEauzEcui830Vpdj1FDYSXhLkQFxZxvJ5YOuFTbIWs7dbBCO1sulKI/DNhri4+BB/aHI4MYn0k0bl2O0q1DhAgMBAAECgYA743drjOkwZBjJ6E/NCODwO+bNFvsvadBhnCeQrm4CP7aErG/BpUWLRgmQH1wpMJ1rT/zLze341FYLVZX2M+q3vlgoTMvJkqA7zfCtzvI+Yq913ZhYFM+wogL6nEthHbeBgFkod5hUe+DNvXZTa4iUm1iaOCxNGxvroQQEOxbK0QJBAOOuZgtpkcUhNAFfO2QBA0OgJNVm06ULAWCi0tk/gewYu5Ga3der5WKc2jTzLJIrJCgDS5ulXj9aTsa03foo9FUCQQCVA/OzAUjYR+QSeqRdHSgkm2vYuZKkFo5ioAR8/ehNNRb9D+wpwfu4y/3EgyZz0T10dto4RmG3GeCAMhlw3lZdAkEA0/p2hZ+XmVrNiY15xSTwPhEm2gzvdhUmBivydVQciY2JbQosC3W+jq6MtonFcJ17/0j6JwKzGfbhqz2QAi4JNQJANETqmoN81cCB06mJNdAgYJbTwXV2ZnAzCY0vhdhaP5q7sZCAOjV84llLbj7CoiVm9Q8rhEnLxLoi8VShb+HNUQJAdTI4DD0Z7MkmBMSN48cgu5TTRp3OqP34mPM1uazGwJ1D3TB/nQehaegEGkFJSaNt4iVIDBD2f4RgwUFOPA8i5Q==
'''
pub_key = '''
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCEiAUtlYa7b6aitkDTjGQt7PT8tGQWNQWsnzzR1LcpHk4GyQ1WvKDSmvbhtbavH05gf93wlbvsn0luIifztPDvlBBGrsxHLovN9FaXY9RQ2El4S5EBcWcbyeWDrhU2yFrO3WwQjtbLpSiPwzYa4uPgQf2hyODGJ9JNG5djtKtQ4QIDAQAB
'''

#rsa_util = RsaUtil(config.apub_key, config.his_pri_key)
rsa_util = RsaUtil(pub_key, pri_key)
#print(f'test: {data}')

encrypt = rsa_util.public_long_encrypt(data)
print(f'test: {encrypt}')
decrypt_str = rsa_util.private_long_decrypt(encrypt)
#print(f'test: {decrypt_str}')

#sign = rsa_util.sign(data)
#print(f'sign: {sign}')

#verify = rsa_util.verify(decrypt_str, sign)
#print(f'verify: {verify}')

'''
header = {}
header["Content-Type"] = "application/json"
data = encrypt
url = "http://sitpay.ciics.cn/tpatest/tpa/getAccounts"
r = requests.post(url,headers=header, data=json.dumps(data))
print(r.content)
'''
