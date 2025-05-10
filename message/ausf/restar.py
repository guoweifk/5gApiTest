#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-05-05 16:25 
@file: restar.py
@project: 5gAPItest
@describe: Powered By GW
"""
import socket
import json
import time
from h2.connection import H2Connection
from h2.config import H2Configuration
from h2.events import ResponseReceived, DataReceived, StreamEnded

# 设置目标（AUSF）
host = '127.0.0.11'
port = 7777

# 准备请求体
payload = {
    "supiOrSuci": "suci-0-001-01-0000-0-0-0000000000",
    "servingNetworkName": "5G:mnc001.mcc001.3gppnetwork.org"
}
body = json.dumps(payload).encode('utf-8')

# 准备 HTTP/2 头部
headers = [
    (':method', 'POST'),
    (':path', '/nausf-auth/v1/ue-authentications'),
    (':scheme', 'http'),
    (':authority', f'{host}:{port}'),
    ('user-agent', 'AMF'),
    ('accept', 'application/3gppHal+json,application/problem+json'),
    ('3gpp-sbi-sender-timestamp', time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())),
    ('3gpp-sbi-max-rsp-time', '10000'),
    ('content-type', 'application/json'),
    ('content-length', str(len(body)))
]

# 建立 TCP 连接
sock = socket.create_connection((host, port))

# 初始化 H2 连接
config = H2Configuration(client_side=True)
conn = H2Connection(config=config)
conn.initiate_connection()
sock.sendall(conn.data_to_send())

# 接收 SETTINGS 帧
data = sock.recv(65535)
conn.receive_data(data)
sock.sendall(conn.data_to_send())

# 创建 stream
stream_id = 1
conn.send_headers(stream_id=stream_id, headers=headers, end_stream=False)
conn.send_data(stream_id=stream_id, data=body, end_stream=True)
sock.sendall(conn.data_to_send())

# 读取响应
response_complete = False
while not response_complete:
    data = sock.recv(65535)
    if not data:
        raise RuntimeError("Connection closed by server.")

    events = conn.receive_data(data)
    for event in events:
        if isinstance(event, ResponseReceived):
            print("Headers:", event.headers)
        elif isinstance(event, DataReceived):
            print("Body:", event.data.decode())
        elif isinstance(event, StreamEnded):
            response_complete = True

# 关闭连接
conn.close_connection()
sock.sendall(conn.data_to_send())
sock.close()
