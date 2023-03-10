#!/usr/bin/env python3

from mosRsa_split import RsaUtil
import json
import config
import testPram
import  ppp


data = "{\"0\":\"0\",\"1\":\"1\",\"10\":\"10\",\"11\":\"11\",\"12\":\"12\",\"13\":\"13\",\"14\":\"14\",\"15\":\"15\",\"16\":\"16\",\"17\":\"17\",\"18\":\"18\",\"19\":\"19\",\"2\":\"2\",\"3\":\"3\",\"4\":\"4\",\"5\":\"5\",\"6\":\"6\",\"7\":\"7\",\"8\":\"8\",\"9\":\"9\"}"
data = "1" * 540
data = """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"""
pri_key = '''
MIICWwIBAAKBgQCQFA4YVQZatJAyO7TsuzkWE8dz17qi8GuOCnegKbKd6alLXkDz
KhVG3kd3GijouHtlqsm2zFCK7K+I5MUu8Fuk23OEwIVZn9StltjLzJ1hB1AZC1/N
CoCFZG5T2+AaQolrw8LvPS5jH2TuYQf7oLDHR88BKJgV/tZlr22Jicqm0wIDAQAB
AoGAMP6A5IlVRdcNCef/2Fi6SuWi96OuleYHzR+GGnLTiJuCtFxy3b27yoOf7cJ5
ktnZLHNtcLn90aA2+OhCnXmiz+M9PNArzfvtDoAKMlM9UEpBjGW/QYPkcHgnKOs9
utAr4OnPB9PFdvCuwya4P8AL/7kpjSW+4zQpUT459BlJFxECQQDYUnQQgyR3CZiG
Pj9vPfmmFmogpZpJTG9zAuOjOCxa5BQvV4iKhk6pkQAaVsjc7WMobEIhLqXn/I8E
ldsqIPj1AkEAqoFZULpjke8CQm0rmr2UdbhU74KKYzeS2KKKc/2TdQUzTqvBdY2+
VCyc0Ok6BWctBHfsu4FR6YpDYsg3QwvjpwJAEHeuaDdjhkBPwSBp+dDw+UjJiXSx
2xSbg1jb9WfoUH7+XmA+f7UbteLY7ChhIBheLQyYuCfx70gVpxa1WW6rJQJAEahR
mpWi6CMLZduub1kAvew4B5HKSRohQAQdOIPjOHQwaw5Ie6cRNeBk4RG2K4cS12qf
/o8W74udDObVKkFZ8wJAPL8bRWv0IWTlvwM14mKxcVf1qCuhkT8GgrG/YP/8fcW8
SiT+DifcA7BVOgQjgbTchSfaA+YNe7A9qiVmA+G4GQ==
'''

rsa_util = RsaUtil(config.apub_key, config.pri_key)
print(f'test: {data}')

#encrypt = rsa_util.public_long_encrypt(data)
#print(f'test: {encrypt}')

encrypt = data
decrypt_str = rsa_util.private_long_decrypt(encrypt)
print(f'test: {decrypt_str}')

#sign = rsa_util.sign(data)
#print(f'sign: {sign}')

#verify = rsa_util.verify(decrypt_str, sign)
#print(f'verify: {verify}')
