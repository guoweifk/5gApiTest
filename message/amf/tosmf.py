#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-05-05 22:49 
@file: tosmf.py
@project: 5gAPItest
@describe: Powered By GW
"""
import socket
import json
import time
from h2.connection import H2Connection
from h2.config import H2Configuration
from h2.events import ResponseReceived, DataReceived, StreamEnded

# -------- 配置部分 --------
host = "127.0.0.200"
port = 7777
stream_id = 1

# 请求体内容
payload = {
    "ueLocation": {
        "nrLocation": {
            "tai": {
                "plmnId": {"mcc": "001", "mnc": "01"},
                "tac": "000001"
            },
            "ncgi": {
                "plmnId": {"mcc": "001", "mnc": "01"},
                "nrCellId": "000000011"
            },
            "ueLocationTimestamp": "2025-05-05T14:47:09.602593Z"
        }
    },
    "ueTimeZone": "+08:00"
}
body = json.dumps(payload).encode("utf-8")

# 构造 HTTP/2 Headers
headers = [
    (':method', 'POST'),
    (':path', '/nsmf-pdusession/v1/sm-contexts/1/release'),
    (':scheme', 'http'),
    (':authority', '127.0.0.200:7777'),
    ('3gpp-sbi-discovery-service-names', 'nsmf-pdusession'),
    ('3gpp-sbi-discovery-target-nf-type', 'SMF'),
    ('3gpp-sbi-sender-timestamp', 'Mon, 05 May 2025 14:47:09.602 GMT'),
    ('3gpp-sbi-target-apiroot', 'http://127.0.0.4:7777'),
    ('3gpp-sbi-max-rsp-time', '10000'),
    ('content-type', 'application/json'),
    ('accept', 'application/json,application/problem+json'),
    ('user-agent', 'AMF'),
    ('content-length', str(len(body)))
]

# -------- 发送逻辑 --------
sock = socket.create_connection((host, port))
conn = H2Connection(config=H2Configuration(client_side=True))
conn.initiate_connection()
sock.sendall(conn.data_to_send())

# 等待 SETTINGS ACK
data = sock.recv(65535)
conn.receive_data(data)
sock.sendall(conn.data_to_send())

# 发送 headers + data
conn.send_headers(stream_id=stream_id, headers=headers, end_stream=False)
conn.send_data(stream_id=stream_id, data=body, end_stream=True)
sock.sendall(conn.data_to_send())

# 接收返回结果
while True:
    data = sock.recv(65535)
    if not data:
        break
    events = conn.receive_data(data)
    for event in events:
        if isinstance(event, ResponseReceived):
            print(f"[Headers] {event.headers}")
        elif isinstance(event, DataReceived):
            print(f"[Body] {event.data.decode()}")
        elif isinstance(event, StreamEnded):
            print(f"Stream {stream_id} ended.")
            sock.close()
            exit(0)
