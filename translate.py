#! /usr/bin/python3.6
# -*-coding:utf-8 -*-

import requests
import hashlib
import random
import sys
import json
from urllib.parse import urlencode

def is_alphabet(uchar):
    '''
    判断一个unicode是否是英文字母
    '''
    if (uchar >= u'\0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def translate(word, from_lang, to_lang):
    '''
    把语言为from_lang的word翻译成to_lang
    return 返回翻译后的文本
    '''
    appid = 20181129000241066
    secretKey = 'sIyV3ohEbeu_ZbpZ0oJi'
    salt = random.randint(32768, 65536)
    
    #获得sign
    sign = str(appid) + word + str(salt) + secretKey
    m = hashlib.md5()
    m.update(sign.encode('utf-8'))
    sign = m.hexdigest()
    #创建dict
    data = {
        'q' : word,
        'from' : from_lang,
        'to' : to_lang,
        'appid' : appid,
        'salt' : salt,
        'sign' : sign,
    }
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate?';
    url += urlencode(data)
    #api调用
    response = requests.get(url)

    return response.text

def main():
    #获取命令行参数
    length = len(sys.argv)

    if length == 1:
        print('请输入要翻译的中文/英语')
        return
    from_lang = ''
    to_lang = ''
    #简单判断是中文还是英文
    if is_alphabet(sys.argv[1][0]):
        from_lang = 'en'
        to_lang = 'zh'
    else:
        from_lang = 'zh'
        to_lang = 'en'

    text = translate(sys.argv[1], from_lang, to_lang)
    d = json.loads(text)

    for result in d['trans_result']:
        print("%s     =>     %s" % (result['src'], result['dst']))

if __name__ == '__main__':
    main()
