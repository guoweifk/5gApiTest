#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-05-06 16:14 
@file: tosmfmodify.py
@project: 5gAPItest
@describe: Powered By GW
"""
import socket
import select
import time
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived, StreamEnded



def build_modify_body(n2SmInfoType):
    boundary_id = "=-HiUnTdspH11t3eo3/2q65A=="
    boundary = f"--{boundary_id}"

    json_part = {
        "n2SmInfo": {"contentId": "ngap-sm"},
        "n2SmInfoType": n2SmInfoType
    }

    import json
    part1 = (
        f"{boundary}\r\n"
        f"Content-Type: application/json\r\n\r\n"
        f"{json.dumps(json_part)}\r\n"
    )

    ngap_hex = "0003e0c0a8371d000000010001"
    ngap_bytes = bytes.fromhex(ngap_hex)

    part2 = (
        f"{boundary}\r\n"
        f"Content-Id: ngap-sm\r\n"
        f"Content-Type: application/vnd.3gpp.ngap\r\n\r\n"
    ).encode('utf-8') + ngap_bytes + b"\r\n"

    closing = f"{boundary}--\r\n"

    full_body = part1.encode('utf-8') + part2 + closing.encode('utf-8')
    return full_body

def build_modify_headers(body, sm_context_id):
    return [
        (':method', 'POST'),
        (':path', f'/nsmf-pdusession/v1/sm-contexts/{sm_context_id}/modify'),
        (':scheme', 'http'),
        (':authority', '127.0.0.4:7777'),
        ('content-type', 'multipart/related; boundary="=-HiUnTdspH11t3eo3/2q65A=="'),
        ('content-length', str(len(body))),
        ('3gpp-sbi-sender-timestamp', 'Mon, 05 May 2025 14:46:59.921 GMT'),
        ('3gpp-sbi-max-rsp-time', '10000'),
        ('user-agent', 'AMF'),
        ('accept', 'application/json,application/problem+json'),
    ]



def send_http2_modify(sm_context_id,n2SmInfoType):
    sock = socket.create_connection(('127.0.0.4', 7777))
    conn = H2Connection()
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())
    body = build_modify_body(n2SmInfoType)
    headers = build_modify_headers(body,sm_context_id)


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
    send_http2_modify(664,"PDU_RES_REL_RSP")
