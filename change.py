#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

'''
python change.py [--encoding=] [--breaker=] [--path=.]
'''

import os
import os.path
import sys
import chardet
import argparse


def split_path(filepath):
    """
    把路径拆分为目录和文件名 文件名可以是虚拟文件名或者不存在
    @param filepath 文件路径
    @return tuple(dirname, filename) 返回(None, None)表示输入路径有误
    """
    dirname, filename = None, None
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

    return (dirname, filename)


def change(dirname, name, newline, encoding):
    """
    先检测文件是否存在
    文件转换断行字符newLine和编码格式
    @param name     文件名(绝对路径)
    @param newline  断行字符
    @param encoding 编码格式
    @return True/False
    """
    filename = os.path.join(dirname, name)
    #获取源编码 为了转换编码
    with open(filename, 'rb') as fp:
        content_bytes = fp.read()
    source_encoding = chardet.detect(content_bytes).get('encoding')
    # 不转换编码
    if encoding is None:
        encoding = source_encoding
    if newline is None:
    	newline = '\n'

    # 以\n换行符打开文件
    with open(filename, 'r', encoding = source_encoding, newline='\n') as fp:
        content_str = fp.read()

    #边写边修改换行符号
    with open(filename, 'w', encoding = encoding, newline=newline) as fp:
        fp.write(content_str)

    return True


def get_args():
    """
    获取命令行参数参数
    """
    parser = argparse.ArgumentParser(description='change files\'s encoding or line break')

    # 解析规则
    parser.add_argument('--encoding', action='store', help='the file\'s new encoding')
    parser.add_argument('--breaker', action='store', help='the file\'s new line break')
    parser.add_argument('--path', action='store', help='the work path or a filename', default='.')

    # 将变量以标签-值得形式字典形式存入args
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    filepath = None
    #获取命令行参数
    args = get_args()
    #都为空时表示输入有误
    if args.encoding is None and args.breaker is None:
        print('--encoding or breaker is necessary!')
        exit()
    # 对path进行操作
    dirname, filename = split_path(args.path)
    #不包含通配符 只能是具体文件
    if filename.find('*') == -1:
        ret = change(dirname, filename, args.breaker, args.encoding)
    else:
        #filename可能的取值"*.*" "*.py"
        file_ext = os.path.splitext(filename)[-1]

        for parent, dirnames, filenames in os.walk(dirname, followlinks = True):
            for name in filenames:
                #满足扩展名
                if file_ext == '.*' or file_ext in name:
                    change(parent, name, args.breaker, args.encoding)
                    print('change %s successful' % name)