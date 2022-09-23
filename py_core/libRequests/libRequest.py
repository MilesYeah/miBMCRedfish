#!/usr/bin/python3

import requests
# from requests_toolbelt import MultipartEncoder
import copy
import json
from typing import Union
import re
import time

from py_core.handlerFile import save_binary_to_file
from py_core.handlerLogger import logger


def chk_response_header_has_attachment(response_headers):
    """确认应答头中是否包含附件信息, 如果有则直接返回文件名"""
    check_compile = re.compile('.*(attachment);.*filename=(.+)')
    for key, value in response_headers.items():
        if key.lower() == 'content-disposition':
            match = check_compile.match(value)
            if match is not None:
                file_name = match.group(2)
                return file_name
    return False


class HTTPRequest:
    potential_methods = ['get', 'post', 'put', 'patch', 'delete', 'fetch', 'options', 'head']
    arguments = ["url", "params", "data", "json", "headers", "cookies", "files", "auth", "timeout", "allow_redirects",
                 "proxies", "verify", "stream", "cert"]

    def __init__(self, **kwargs):
        """
        :param url: URL for the new :class:`Request` object.
        :param params: (optional)
            Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param data: (optional)
            Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional)
            A JSON serializable Python object to send in the body of the :class:`Request`.
        :param headers: (optional)
            Dictionary of HTTP Headers to send with the :class:`Request`.
        :param cookies: (optional)
            Dict or CookieJar object to send with the :class:`Request`.
        :param files: (optional)
            Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
            ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
            or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
            defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
            to add for the file.
        :param auth: (optional)
            Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional)
            How many seconds to wait for the server to send data
            before giving up, as a float, or a :ref:`(connect timeout, read
            timeout) <timeouts>` tuple.
            :type timeout: float or tuple
        :param allow_redirects: (optional)
            Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
            :type allow_redirects: bool
        :param proxies: (optional)
            Dictionary mapping protocol to the URL of the proxy.
        :param verify: (optional)
            Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
        :param stream: (optional)
            if ``False``, the response content will be immediately downloaded.
        :param cert: (optional)
            if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        """
        self.kwargs = kwargs
        self.response = None

    def get_url(self):
        return self.kwargs.get('url')

    def set_url(self, v):
        self.kwargs['url'] = v

    def get_method(self):
        return self.kwargs.get('method', 'get')

    def set_method(self, method):
        method = str(method).strip().lower()
        if method not in self.potential_methods:
            raise ValueError(f"Wrong method({method}) is set, potential values:({self.potential_methods})")
        else:
            self.kwargs['method'] = method

    def get_headers(self):
        return self.kwargs.get('headers')

    def set_headers(self, v):
        self.kwargs['headers'] = v

    url = property(get_url, set_url, doc="Setup url for current HTTPRequest object.")
    method = property(get_method, set_method, doc="Setup method for current HTTPRequest object.")
    headers = property(get_headers, set_headers, doc="Setup headers for current HTTPRequest object.")

    ##############################################################################################
    # request actoins
    @property
    def request_body(self):
        """处理请求体"""
        return {
            'status_code': self.resp_st_code,
            'data': str(self.response.request.body),  # 文件上传请求response.request.body类型为bytes,需要转化为str
        }

    @property
    def request_headers(self):
        """处理请求头"""
        request_headers = copy.deepcopy(self.response.request.headers)
        return dict(request_headers)  # CaseInsensitiveDict转为Dict

    def send(self, **kwargs) -> requests.Response:
        for k, v in kwargs.items():
            self.kwargs[k.strip().lower()] = v.strip() if isinstance(v, str) else v

        a = requests.session()
        argus = {k: v for k, v in self.kwargs.items() if k != 'method' }
        self.response = None
        if re.findall('get', self.method, re.I):
            self.response = requests.get(**argus)
        elif re.findall('post', self.method, re.I):
            self.response = requests.post(**argus)
        elif re.findall('delete', self.method, re.I):
            self.response = requests.delete(**argus)
        elif re.findall('put', self.method, re.I):
            self.response = requests.put(**argus)
        elif re.findall('patch', self.method, re.I):
            self.response = requests.patch(**argus)
        elif re.findall('options', self.method, re.I):
            self.response = requests.options(**argus)
        elif re.findall('head', self.method, re.I):
            self.response = requests.head(**argus)
        else:
            raise ValueError("Request method is not set.")
        logger.info(f"Sending request: {json.dumps(self.kwargs, indent=4)}.")
        return self.response

    ############################################################################################
    # response actions
    @property
    def resp_st_code(self):
        return self.response.status_code

    # 获取接口的全部响应时间
    @property
    def resp_elapsed_time(self):
        return self.response.elapsed.total_seconds()

    @property
    def resp_headers(self):
        """处理应答头"""
        response_headers = copy.deepcopy(self.response.headers)  # dict()方法是不是会重新创建一个新的对象 ,实际为浅复制
        response_headers['status_code'] = self.resp_st_code
        response_headers['elapsed_time'] = self.resp_elapsed_time
        return dict(response_headers)  # CaseInsensitiveDict转为Dict

    @property
    def resp_body(self):
        """处理应答体"""
        # resp_body = self.response.content.decode(self.response.apparent_encoding)
        try:
            if self.response.content:
                file_name = chk_response_header_has_attachment(self.resp_headers)
                if file_name:  # 响应头标识为附件
                    resp_body = str(self.response.content)[2:-1]
                    # 比如 "b'PK\x03\x04....\x14\x00'" -> "PK\x03\x04....\x14\x00"
                    save_binary_to_file(bytes=self.response.content, fpn=file_name)
                    logger.info(f"Response body is a file which is stored in {file_name}")
                else:
                    resp_body = json.loads(self.response.content)
                    logger.info(f"Response body: {json.dumps(resp_body, indent=4)}")
            else:
                resp_body = ''
            return resp_body
        except json.JSONDecodeError:
            # www.baidu.com 避免应答乱码
            # try:
            #     resp_body = self.response.content.decode(self.response.encoding)
            # except (UnicodeDecodeError, TypeError):
            #     resp_body = self.response.content.decode(self.response.apparent_encoding)
            try:
                resp_body = self.response.content.decode(self.response.apparent_encoding)
            except (UnicodeDecodeError, TypeError):
                resp_body = self.response.content.decode(self.response.encoding)
            logger.info(f"Response body: {json.dumps(resp_body, indent=4)}")
            return resp_body

    ############################################################################################
    # test actions
    def chk_resp_st_code(self, st_code):
        if self.resp_st_code == st_code:
            return True


if __name__ == '__main__':
    url = "https://v0.yiketianqi.com/api"
    paras ={"version": "v61",
            "appid": "45164426",
            "appsecret": "fWnVlW1c",
            "city": "广水"
            }
    a = HTTPRequest()
    a.url = url
    resp = a.send("get")

    print()
