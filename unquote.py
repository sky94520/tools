#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

import os
import sys
from urllib.parse import unquote

argument = None
#有参数，则仅取第一个
if len(sys.argv) > 1:
    argument = sys.argv[1]

L = None

if os.path.isdir(argument):
    L = os.listdir(argument)
else:
    L = [argument]

print(L)

#开始改名
for name in L:
    if name == 'uquote.py':
        continue
    trueName = unquote(name)

    if trueName == name:
        continue
    os.rename(name, trueName)
    print('%s=>:%s成功' % (name, trueName))
