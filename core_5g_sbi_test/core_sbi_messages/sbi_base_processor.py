#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-03 22:36 
@file: sbi_base_processor.py
@project: 5gAPItest
@describe: Powered By GW
"""


class SBIBaseProcessor:
    def __init__(self, connection):
        self.connection = connection

    # =========  消息方向元数据 =========
    @property
    def sender(self) -> str:
        raise NotImplementedError("Must define sender NF name, e.g. 'AMF'")

    @property
    def receiver(self) -> str:
        raise NotImplementedError("Must define receiver NF name, e.g. 'UDM'")

    # ========= Client 使用 =========
    def build_headers(self, body=None):
        raise NotImplementedError

    def build_body(self):
        return b''

    def send(self):
        body = self.build_body()
        headers = self.build_headers(body)
        stream_id = self.connection.send_stream(headers, body)
        print(f"[SENT] {self.sender} → {self.receiver} | stream={stream_id}")
        self.connection.wait_response(stream_id)

    # ========= Server 使用 =========
    def match(self, path: str) -> bool:
        """服务端：判断是否处理该请求"""
        raise NotImplementedError

    def handle(self, stream_id: int, conn, headers: list):
        """服务端：构造响应,返回对应的头和消息体"""
        raise NotImplementedError
