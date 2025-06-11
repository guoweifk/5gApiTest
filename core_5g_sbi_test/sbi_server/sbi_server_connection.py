#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-04 14:55 
@file: sbi_server_connection.py
@project: 5gAPItest
@describe: Powered By GW
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

import socket
from h2.connection import H2Connection
from h2.config import H2Configuration
from core_5g_sbi_test.sbi_server.sbi_server_dispatcher import dispatch


def run_server(host='127.0.0.12', port=7777):
    server_sock = socket.socket()
    server_sock.bind((host, port))
    server_sock.listen(5)
    print(f"[MOCK-SBI] Server running on {host}:{port}")

    while True:
        sock, addr = server_sock.accept()
        print(f"[MOCK-SBI] New connection from {addr}")
        conn = H2Connection(config=H2Configuration(client_side=False))
        conn.initiate_connection()
        sock.sendall(conn.data_to_send())

        while True:
            try:
                data = sock.recv(65535)
                if not data:
                    break
                events = conn.receive_data(data)

                for event in events:
                    if hasattr(event, "headers"):
                        headers = dict(event.headers)
                        path = headers.get(':path', '')
                        print(f"path: {path}")
                        stream_id = event.stream_id

                        processor = dispatch(path, headers)
                        if processor:
                            headers, body = processor.handle(stream_id, conn, headers)
                            conn.send_headers(stream_id, headers, end_stream=(not body))
                            if body:
                                conn.send_data(stream_id, body, end_stream=True)
                            sock.sendall(conn.data_to_send())
                        else:
                            print(f"[WARN] No processor for path: {path}")
            except Exception as e:
                print(f"[ERROR] {e}")
                break

        sock.close()


if __name__ == '__main__':
    run_server()
