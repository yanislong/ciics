#!/usr/bin/env python3

import qrcode

#img = qrcode.make("https://h5.smartensurehealth.cn/#/activationEquity?activationCode=bfHPcQDx")
codetest = "676DAPA5"
img = qrcode.make("http://sitsehwx.ciics.cn/#/activationEquity?activationCode=" + codetest)

with open(codetest + '.png','wb') as f:
    img.save(f)

