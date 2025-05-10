#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-04-25 22:31 
@file: sdm_sub.py
@project: 5gAPItest
@describe: Powered By GW
"""
import socket
import time
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived, StreamEnded
from h2.config import H2Configuration
import json
# Payload 构造
payload = {
    "nfInstanceId": "fc9a42c4-21da-41f0-9882-13a195797c37",
    "implicitUnsubscribe": True,
    "callbackReference": "http://127.0.0.4:7777/nsmf-callback/v1/sdmsubscription-notify/imsi-001010000000000",
    "monitoredResourceUris": ["imsi-001010000000000/sm-data"],
    "singleNssai": {"sst": 1},
    "dnn": "internet",
    "plmnId": {"mcc": "001", "mnc": "01"},
    "supportedFeatures": "1000",
    "uniqueSubscription": True
}

body = json.dumps(payload).encode()

headers = [
    (':method', 'POST'),
    (':path', '/nudm-sdm/v2/imsi-001010000000000/sdm-subscriptions'),
    (':scheme', 'http'),
    (':authority', '127.0.0.200:7777'),
    ('accept', 'application/json,application/problem+json'),
    ('3gpp-sbi-sender-timestamp', 'Fri, 25 Apr 2025 13:41:47.181 GMT'),
    ('3gpp-sbi-target-apiroot', 'http://127.0.0.12:7777'),
    ('3gpp-sbi-max-rsp-time', '10000'),
    ('3gpp-sbi-discovery-service-names', 'nudm-sdm'),
    ('content-type', 'application/json'),
    ('user-agent', 'SMF'),
    ('3gpp-sbi-discovery-target-nf-type', 'UDM'),
    ('content-length', str(len(body)))  # 建议动态设置
]


host = "127.0.0.4"
port = 7777

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

    except Exception as e:
        print(f"Error: {e}, reconnecting...")
        try:
            sock.close()
        except:
            pass
        continue
