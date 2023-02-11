#! /usr/bin/env python 2.7.11
#coding=utf-8
#本脚本改造成opencl,使用NVIDIA GeForce GTX 750 Ti来全速测试,每秒仅能达到500H /s
import hashlib
from base64 import b64encode, b64decode
import struct

workbookAlgorithmName="SHA-512"
workbookHashValue="CUk11CE58maVR6WJkSe5zyBiUyyZVknM5GO3zu3dTpVzaWnkYkPJ1s1rbjkJ0Bgnzpy0n/dwx3/lgypVA/W3gg=="
workbookSaltValue="ghbhds+wWLP6D70v0xoErQ=="
workbookSpinCount="100000"

def findpassword(password):
    alg = workbookAlgorithmName.replace('-', '').lower()
    # if alg not in hashlib.algorithms:
    #     raise Exception("Algorithm %s not in %r" % (alg, hashlib.algorithms))
    alg = getattr(hashlib, alg)
    count = int(workbookSpinCount)
    digests = []
    salt = workbookSaltValue
    salt = b64decode(salt)
    
    m = alg()
    m.update(salt) # data is binary, length = 16
    m.update(password.encode('utf-16-le')) # window's "unicode" encoding
    h = m.digest()
    #这里的十万次迭代循环加密,能慢到吐血
    #平时加密和取消密码,时间很短暂,几乎很难感觉到,但对爆破却是致命的打击
    for i in range(count):
        m = alg()
        m.update(h)
        m.update(struct.pack("<I", i)) # little endian 4-byte unsigned integer iterator
        h = m.digest()
    digest = b64encode(h)
    print(digest)
    print("log:", digest, "密码找到了" if digest == workbookHashValue else "密码不正确")

if __name__ == '__main__':
    #这里可以使用字典
    findpassword("bugscaner")