#!/usr/bin/env python3

#生成秘钥
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5

import base64

random_generator = Random.new().read
rsa = RSA.generate(1024, random_generator)
private_pem = rsa.exportKey()

with open('private.pem','wb') as f:
    f.write(private_pem)
    public_pem = rsa.publickey().exportKey()

with open('public.pem','wb') as f:
    f.write(public_pem)

#加密数据
def encryp(message):
    with open('public.pem','r') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        endata = base64.b64encode(cipher.encrypt(message.encode(encoding="utf-8")))
        data = endata.decode("utf-8")
        print(data)
        return data

#解密数据
def decryp(message):
    with open('private.pem','r') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        text = cipher.decrypt(base64.b64decode(message), "ERROR")
        print(text)
        return True

if __name__ == "__main__":
    res = encryp('{"test":"abc"}')
    decryp(res)
