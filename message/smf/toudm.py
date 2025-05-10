#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-05-05 22:20 
@file: toudm.py
@project: 5gAPItest
@describe: Powered By GW
"""
import socket
import json
import time
from h2.connection import H2Connection
from h2.config import H2Configuration
from h2.events import ResponseReceived, DataReceived, StreamEnded

# 请求目标（SCP）
host = "127.0.0.200"
port = 7777

# 构造 JSON payload
payload = {
    "smfInstanceId": "c3c4044c-29b1-41f0-9412-0def06b5189a",
    "pduSessionId": 1,
    "singleNssai": { "sst": 1 },
    "dnn": "internet",
    "plmnId": { "mcc": "001", "mnc": "01" }
}
body = json.dumps(payload).encode("utf-8")

# 构造 HTTP/2 头部
headers = [
    (':method', 'PUT'),
    (':path', '/nudm-uecm/v1/imsi-001010000000000/registrations/smf-registrations/1'),
    (':scheme', 'http'),
    (':authority', '127.0.0.200:7777'),
    ('content-type', 'application/json'),
    ('user-agent', 'SMF'),
    ('accept', 'application/json,application/problem+json'),
    ('3gpp-sbi-sender-timestamp', 'Mon, 05 May 2025 14:05:02.751 GMT'),
    ('3gpp-sbi-target-apiroot', 'http://127.0.0.12:7777'),
    ('3gpp-sbi-discovery-target-nf-type', 'UDM'),
    ('3gpp-sbi-discovery-service-names', 'nudm-uecm'),
    ('3gpp-sbi-max-rsp-time', '10000'),
    ('content-length', str(len(body)))
]

# 构造 HTTP/2 请求头（DELETE）
headers2 = [
    (':method', 'DELETE'),
    (':path', '/nudm-uecm/v1/imsi-001010000000000/registrations/smf-registrations/1'),
    (':scheme', 'http'),
    (':authority', '127.0.0.200:7777'),
    ('user-agent', 'SMF'),
    ('accept', 'application/problem+json'),
    ('3gpp-sbi-discovery-target-nf-type', 'UDM'),
    ('3gpp-sbi-discovery-service-names', 'nudm-uecm'),
    ('3gpp-sbi-sender-timestamp', 'Mon, 05 May 2025 14:47:09.614 GMT'),
    ('3gpp-sbi-target-apiroot', 'http://127.0.0.12:7777'),
    ('3gpp-sbi-max-rsp-time', '10000')
]

while True:
    try:
        sock = socket.create_connection((host, port))

        config = H2Configuration(client_side=True)
        conn = H2Connection(config=config)
        conn.initiate_connection()
        sock.sendall(conn.data_to_send())

        # 等待服务端 SETTINGS ACK
        data = sock.recv(65535)
        conn.receive_data(data)
        sock.sendall(conn.data_to_send())

        stream_id = 1  # 正确从1开始

        while True:
            conn.send_headers(stream_id=stream_id, headers=headers, end_stream=False)
            conn.send_data(stream_id=stream_id, data=body, end_stream=True)
            sock.sendall(conn.data_to_send())

            print(f"Sent stream {stream_id}")

            stream_ended = False
            while not stream_ended:
                data = sock.recv(65535)
                if not data:
                    raise Exception("Connection closed by server.")
                events = conn.receive_data(data)
                for event in events:
                    if isinstance(event, ResponseReceived):
                        print(f"Stream {stream_id} Response headers:", event.headers)
                    elif isinstance(event, DataReceived):
                        print(f"Stream {stream_id} Response body:", event.data.decode())
                    elif isinstance(event, StreamEnded):
                        print(f"Stream {stream_id} ended.")
                        stream_ended = True



            stream_id += 2
            time.sleep(0.1)

            conn.send_headers(stream_id=stream_id, headers=headers2, end_stream=False)
            sock.sendall(conn.data_to_send())
            print(f"Sent stream {stream_id}")
            stream_ended = False

            stream_id += 2
            time.sleep(0.1)




    except Exception as e:
        print(f"Error: {e}, reconnecting...")
        try:
            sock.close()
        except:
            pass
        continue
