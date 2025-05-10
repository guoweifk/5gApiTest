#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-04-25 15:14 
@file: test.py
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
    "supi": "imsi-001010000000000",
    "pduSessionId": 1,
    "pduSessionType": "IPV4",
    "chargingcharacteristics": "00000800",
    "dnn": "internet",
    "notificationUri": "http://127.0.0.4:7777/nsmf-callback/v1/sm-policy-notify/44",
    "ratType": "NR",
    "servingNetwork": {
        "mcc": "001",
        "mnc": "01"
    },
    "userLocationInfo": {
        "nrLocation": {
            "tai": {
                "plmnId": {"mcc": "001", "mnc": "01"},
                "tac": "000001"
            },
            "ncgi": {
                "plmnId": {"mcc": "001", "mnc": "01"},
                "nrCellId": "000000010"
            },
            "ueLocationTimestamp": "2025-04-25T05:47:22.833314Z"
        }
    },
    "ueTimeZone": "+08:00",
    "ipv4Address": "10.45.0.6",
    "subsSessAmbr": {
        "uplink": "1000000 Kbps",
        "downlink": "1000000 Kbps"
    },
    "subsDefQos": {
        "5qi": 9,
        "arp": {
            "priorityLevel": 8,
            "preemptCap": "NOT_PREEMPT",
            "preemptVuln": "NOT_PREEMPTABLE"
        },
        "priorityLevel": 8
    },
    "sliceInfo": {
        "sst": 1
    },
    "suppFeat": "4000000"
}

# ✅ 目标地址（服务器）
remote_ip = "127.0.0.13"
remote_port = 7777

# ✅ 本地发起连接的源 IP 和端口
local_ip = "127.0.0.200"   # 你要从哪个IP发出
local_port = 7777       # 本地源端口（避免冲突）

while True:
    try:
        # ✅ 自定义 socket 实例，绑定源 IP 和端口
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((local_ip, local_port))  # 绑定本地地址
        sock.connect((remote_ip, remote_port))  # 连接目标服务


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
            body = json.dumps(payload).encode()
            headers = [
                (':method', 'POST'),
                (':path', '/npcf-smpolicycontrol/v1/sm-policies'),
                (':scheme', 'http'),
                (':authority', '127.0.0.13:7777'),
                ('3gpp-sbi-discovery-service-names', 'npcf-smpolicycontrol'),
                ('content-type', 'application/json'),
                ('user-agent', 'SMF'),
                ('3gpp-sbi-discovery-target-nf-type', 'PCF'),
                ('accept', 'application/json,application/problem+json'),
                ('3gpp-sbi-sender-timestamp', 'Fri, 25 Apr 2025 13:41:42.106 GMT'),
                ('3gpp-sbi-target-apiroot', 'http://127.0.0.13:7777'),
                ('3gpp-sbi-max-rsp-time', '10000'),
                ('content-length', str(len(body)))
            ]

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




