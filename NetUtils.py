#! python3
# coding=utf-8


import urllib.request
import urllib.parse
import gzip
import re
from io import BytesIO


class NetUtils:

    @staticmethod
    def gen_proxy(protocol, ip, port):
        return {protocol, protocol + '://' + ip + ':' + str(port)}

    #
    # brief: request
    # param: url     str
    # param: data    list
    # param: head    dict
    # param: method  str
    # param: timeout int   second
    # param: proxy   dict
    @staticmethod
    def request(url, data=None, head=None, method='GET', timeout=5, proxy=None):
        retry = 0
        ret = dict()
        resp = None
        if head is None:
            head = dict()
        while retry < 3:
            try:
                req = urllib.request.Request(url, data=data, headers=head, method=method)
                if proxy is not None:
                    proxy_handler = urllib.request.ProxyHandler(proxy)
                    opener = urllib.request.build_opener(proxy_handler)
                    urllib.request.install_opener(opener)
                    resp = urllib.request.urlopen(req, timeout=timeout)
                else:
                    resp = urllib.request.urlopen(req, timeout=timeout)
                resp_data = resp.read()
                ret['data'] = resp_data
                ret['session'] = resp.info()
                ret['result'] = True
                resp.close()
                break
            except Exception as e:
                print(str(e), e.with_traceback())
                if resp is not None:
                    resp.close()
                retry += 1
        return ret

    @staticmethod
    def get_content_charset(session):
        return session.get_content_charset()

    @staticmethod
    def gzip_decode(raw, charset):
        try:
            buff = BytesIO(raw)
            f = gzip.GzipFile(fileobj=buff)
            if charset is not None:
                ret = f.read().decode(charset)
            else:
                print('not set param[charset], decode with gbk')
                ret = f.read().decode('gbk')
        except Exception as e:
            print(str(e), e.with_traceback())
            ret = None
        return ret

    @staticmethod
    def get_value_from_session(session, key):
        regexp = r'{}=[\w\W]*?;'.format(key)
        pat = re.compile(regexp)
        key_value = pat.findall(session)
        if len(key_value) > 0:
            value = key_value[0][len(key) + 1: len(key_value[0]) - 1]
        else:
            value = None
        return value

    @staticmethod
    def decode(html_raw, charset='gbk'):
        return html_raw.decode(charset)
