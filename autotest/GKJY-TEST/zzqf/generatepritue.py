#!/usr/bin/env python

import json
from PIL import Image, ImageDraw   
import os, time, random
import numpy as np
import matplotlib.pyplot as plt

def generate_image(memory_size, filename):
   """
   :param memory_size: 生成图片的大小，单位是m
   param filename: 生成图片的文件格式
   :return:
   """
   filename = './dockerdir/'+ time.strftime('%Y%m%d%H%M%S') +'_'+ str(memory_size) + 'M' '.'+filename
   # 计算所需的像素数量
   num_pixels = (memory_size * 1024.0 * 1024.0) // 3.0  # 每个像素占用 3 个字节（RGB模式）
   print(num_pixels)
   # 根据像素数量计算图片的长和宽
   img_width = int(np.sqrt(num_pixels))
   img_height = int(num_pixels / img_width)
   # 创建一个随机颜色的数组
   pixels = np.random.randint(0, 256, (img_height, img_width, 3), dtype=np.uint8)
   # 根据数组创建图片对象
   image = Image.fromarray(pixels, 'RGB')
   image.save(filename)

#fig = plt.figure(figsize=(100, 100), dpi=100)
# 在这里添加绘图代码
#fig.savefig('dockerdir/output.png')
#os.system("dd if=/dev/zero of=fks1.jpeg bs=2M count=1")
#im = Image.open('fks1.jpeg')
#out_im = im.resize((4500,4500),Image.ANTIALIAS)
#out_im.save('dockerdir/fff2.jpeg')
#im.show()
#print(im.format,im.size,im.mode)
#new_im = im.convert('L',(0.412152,0.523423,0,0.23523,0.1234,0.23423,0,0.23423,0.4222,0.123,0.234,0))
#print(new_im.info)
#im2 = Image.new('RGB',(1000,1000),'#EE00DD')
#draw = ImageDraw.Draw(im2)
#text = "abcdefghij" * 1024 * 1024
#draw.text((20,20),text,fill=(155,55,155))
#im2.save('dockerdir/fuk9.jpeg')

if __name__ == "__main__":
    generate_image(2.9,'png')
