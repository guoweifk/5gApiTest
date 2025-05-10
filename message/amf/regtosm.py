#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-05-06 10:07 
@file: regtosm.py
@project: 5gAPItest
@describe: Powered By GW
"""
import socket
import select
import time
import re
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived, StreamEnded

def build_http2_headers():
    return [
        (':method', 'POST'),
        (':path', '/nsmf-pdusession/v1/sm-contexts'),
        (':scheme', 'http'),
        (':authority', '127.0.0.4:7777'),
        ('content-type', 'multipart/related; boundary="=-HiUnTdspH11t3eo3/2q65A=="'),
        ('accept', 'application/json,application/vnd.3gpp.ngap,application/problem+json'),
        ('3gpp-sbi-sender-timestamp', 'Mon, 05 May 2025 14:46:59.881 GMT'),
        ('3gpp-sbi-max-rsp-time', '10000'),
        ('3gpp-sbi-callback', 'Nsmf_PDUSession_StatusNotify'),
        ('user-agent', 'AMF')
    ]

def build_multipart_body():
    boundary = "--=-HiUnTdspH11t3eo3/2q65A=="
    nas_hex = "2e0101c1ffff91a12801007b000780000a00000d00"
    nas_bytes = bytes.fromhex(nas_hex)

    json_part = {
        "supi": "imsi-001010000000000",
        "pei": "imeisv-4370816125816151",
        "pduSessionId": 1,
        "dnn": "internet",
        "sNssai": {"sst": 1},
        "servingNfId": "8cc32472-2b1a-41f0-9850-cd0337c651ed",
        "guami": {"plmnId": {"mcc": "001", "mnc": "01"}, "amfId": "020040"},
        "servingNetwork": {"mcc": "001", "mnc": "01"},
        "n1SmMsg": {"contentId": "5gnas-sm"},
        "anType": "3GPP_ACCESS",
        "ratType": "NR",
        "ueLocation": {
            "nrLocation": {
                "tai": {"plmnId": {"mcc": "001", "mnc": "01"}, "tac": "000001"},
                "ncgi": {"plmnId": {"mcc": "001", "mnc": "01"}, "nrCellId": "000000010"},
                "ueLocationTimestamp": "2025-05-05T14:46:59.599044Z"
            }
        },
        "ueTimeZone": "+08:00",
        "smContextStatusUri": "http://127.0.0.5:7777/namf-callback/v1/imsi-001010000000000/sm-context-status/1",
        "pcfId": "8cc40590-2b1a-41f0-a50a-09159fb4ca15"
    }

    import json
    part1 = (
        f"{boundary}\r\n"
        f"Content-Type: application/json\r\n\r\n"
        f"{json.dumps(json_part)}\r\n"
    )
    part2 = (
        f"{boundary}\r\n"
        f"Content-Id: 5gnas-sm\r\n"
        f"Content-Type: application/vnd.3gpp.5gnas\r\n\r\n"
    ).encode('utf-8') + nas_bytes + b"\r\n"
    closing = f"{boundary}--\r\n"

    full_body = part1.encode('utf-8') + part2 + closing.encode('utf-8')
    return full_body

def send_http2_request():
    sock = socket.create_connection(('127.0.0.4', 7777))
    conn = H2Connection()
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())

    headers = build_http2_headers()
    body = build_multipart_body()
    stream_id = 1

    conn.send_headers(stream_id, headers)
    conn.send_data(stream_id, body, end_stream=True)
    sock.sendall(conn.data_to_send())
    print(f"Sent stream {stream_id}")

    sm_context_id = None
    timeout_seconds = 1.0
    start_time = time.time()
    stream_ended = False

    while not stream_ended:
        elapsed = time.time() - start_time
        if elapsed > timeout_seconds:
            print(f"[Timeout] No response within {timeout_seconds} seconds. Exiting.")
            break

        ready = select.select([sock], [], [], timeout_seconds - elapsed)
        if ready[0]:
            data = sock.recv(65535)
            if not data:
                raise Exception("Connection closed by server.")

            events = conn.receive_data(data)
            for event in events:
                if isinstance(event, ResponseReceived):
                    print(f"Stream {stream_id} Response headers:", event.headers)
                    for name, value in event.headers:
                        if name == b'location':
                            match = re.search(rb'/sm-contexts/(\d+)', value)
                            if match:
                                sm_context_id = int(match.group(1))
                                print(f"Extracted smContextId: {sm_context_id}")
                elif isinstance(event, DataReceived):
                    print(f"Stream {stream_id} Response body:", event.data.decode(errors='ignore'))
                elif isinstance(event, StreamEnded):
                    print(f"Stream {stream_id} ended.")
                    stream_ended = True
        else:
            print(f"[Timeout] No data received. Exiting.")
            break

    sock.close()
    return sm_context_id

if __name__ == '__main__':
    while True:
        result = send_http2_request()
        time.sleep(1)

