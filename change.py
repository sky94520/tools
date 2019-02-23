#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

'''
change.py [windows | linux] '/home/ren/*.*' 对/home/ren/下的所有文件进行转换
对于带有通配符的需要加上单引号 否则shell会对通配符进行展开
'''

import os
import os.path
import sys
import chardet

def split_path(filepath):
    '''
    把路径拆分为目录和文件名 文件名可以是虚拟文件名或者不存在
    @param filepath 文件路径
    @return tuple(dirname, filename) 返回(None, None)表示输入路径有误
    '''
    dirname = None
    filename = None
    #是否是目录
    if os.path.isdir(filepath):
        dirname = filepath
        filename = "*.*"
    else:
        #尝试拆分
        dirname, filename = os.path.split(filepath)
        #目录合法
        if os.path.isdir(dirname):
            #获取角色路径
            dirname = os.path.abspath(dirname)
            if len(filename) == 0:
                filename = '*.*'
        else:
            dirname = None
            filename = None

    return (dirname, filename)

def change(dirname, name, newline, encoding):
    '''
    先检测文件是否存在
    文件转换断行字符newLine和编码格式
    @param name     文件名(绝对路径)
    @param newline  断行字符
    @param encoding 编码格式
    @return True/False
    '''
    if newline == '\r\n':
        oldNewline = '\n'
    else:
        oldNewline = '\r\n'
    filename = os.path.join(dirname, name)
    #获取源编码
    with open(filename, 'rb') as fp:
        content_bytes = fp.read()

    source_encoding = chardet.detect(content_bytes).get('encoding')

    with open(filename, 'r', encoding = source_encoding) as fp:
        content_str = fp.read()

    with open(filename, 'w', encoding = encoding) as fp:
        #边写边修改符号
        fp.write(content_str.replace(oldNewline, newline))

if __name__ == '__main__':
    #TODO:不同平台下的默认编码、断行字符的映射
    mapping = {}
    mapping['windows'] = ('\r\n', 'gb2312')
    mapping['linux'] = ('\n', 'utf-8')
    #获取平台
    platform = sys.argv[1]
    filepath = None
    #获取工作路径
    if len(sys.argv) > 2:
        filepath = sys.argv[2]
    else:
        filepath = os.path.abspath('.')
    
    dirname, filename = split_path(filepath)
    #输入有误
    if dirname is None and filename is None:
        print('输入路径有误，请重试')
        exit()
    #不包含通配符 只能是具体文件
    if filename.find('*') == -1:
        ret = change(dirname, filename, mapping[platform][0], mapping[platform][1])
    else:
        #filename可能的取值"*.*" "*.py"
        file_ext = os.path.splitext(filename)[-1]

        for parent, dirnames, filenames in os.walk(dirname, followlinks = True):
            for name in filenames:
                #满足扩展名
                if file_ext == '.*' or file_ext in name:
                    change(parent, name, mapping[platform][0], mapping[platform][1])
