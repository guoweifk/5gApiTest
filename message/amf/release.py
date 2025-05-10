#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-05-07 15:49 
@file: release.py
@project: 5gAPItest
@describe: Powered By GW
"""
import socket
import select
import time
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived, StreamEnded
import datetime
import json


def build_release_body():
    now_utc = datetime.datetime.utcnow().isoformat() + "Z"

    json_part = {
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
                "ueLocationTimestamp": now_utc
            }
        },
        "ueTimeZone": "+08:00"
    }

    return json.dumps(json_part).encode('utf-8')

def build_release_headers(body, sm_context_id):
    return [
        (':method', 'POST'),
        (':path', f'/nsmf-pdusession/v1/sm-contexts/{sm_context_id}/release'),
        (':scheme', 'http'),
        (':authority', '127.0.0.4:7777'),
        ('content-type', f'application/json'),
        ('content-length', str(len(body))),
        ('3gpp-sbi-sender-timestamp', datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")),
        ('3gpp-sbi-max-rsp-time', '10000'),
        ('user-agent', 'AMF'),
        ('accept', 'application/json,application/problem+json'),
    ]

def send_http2_release(sm_context_id):
    sock = socket.create_connection(('127.0.0.4', 7777))
    conn = H2Connection()
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())
    body = build_release_body()
    headers = build_release_headers(body, sm_context_id)

    stream_id = 1

    conn.send_headers(stream_id, headers)
    conn.send_data(stream_id, body, end_stream=True)
    sock.sendall(conn.data_to_send())
    print(f"Sent stream {stream_id}")

    stream_ended = False
    # Wait for response (optional)

    timeout_seconds = 1.0
    start_time = time.time()
    stream_ended = False

    while not stream_ended:
        elapsed = time.time() - start_time
        if elapsed > timeout_seconds:
            print(f"[Timeout] No response within {timeout_seconds} seconds. Exiting.")
            break

        # Use select to wait up to (remaining time) for data
        ready = select.select([sock], [], [], timeout_seconds - elapsed)
        if ready[0]:
            data = sock.recv(65535)
            if not data:
                raise Exception("Connection closed by server.")

            events = conn.receive_data(data)
            for event in events:
                if isinstance(event, ResponseReceived):
                    print(f"Stream {stream_id} Response headers:", event.headers)
                elif isinstance(event, DataReceived):
                    print(f"Stream {stream_id} Response body:", event.data.decode(errors='ignore'))
                elif isinstance(event, StreamEnded):
                    print(f"Stream {stream_id} ended.")
                    stream_ended = True
        else:
            print(f"[Timeout] No data received. Exiting.")
            break
    stream_id += 2
    time.sleep(0.1)

if __name__ == '__main__':
    send_http2_release(206)
