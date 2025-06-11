#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-03 22:49 
@file: run_sbi_sequence.py
@project: 5gAPItest
@describe: Powered By GW
"""

import socket
import select
import time
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived, StreamEnded

# todo:增加连接池
class SBIConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = H2Connection()
        self.sock = socket.create_connection((host, port))
        self.conn.initiate_connection()
        self.sock.sendall(self.conn.data_to_send())
        self.next_stream_id = 1

    def get_next_stream_id(self):
        stream_id = self.next_stream_id
        self.next_stream_id += 2  # HTTP/2 client-initiated streams are odd numbers
        return stream_id

    def close(self):
        self.sock.close()

    def send_stream(self, headers, body=b'', stream_id=None):
        if stream_id is None:
            stream_id = self.get_next_stream_id()

        end_stream = not body
        self.conn.send_headers(stream_id, headers, end_stream=end_stream)
        if body:
            self.conn.send_data(stream_id, body, end_stream=True)
        self.sock.sendall(self.conn.data_to_send())

        return stream_id

    def wait_response(self, stream_id, timeout=3.0):
        start_time = time.time()
        stream_ended = False

        while not stream_ended:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                print(f"[ERROR] Timeout waiting for stream {stream_id}")
                break

            ready = select.select([self.sock], [], [], timeout - elapsed)
            if ready[0]:
                data = self.sock.recv(65535)
                if not data:
                    raise Exception("Connection closed")

                events = self.conn.receive_data(data)
                for event in events:
                    if hasattr(event, 'stream_id') and event.stream_id != stream_id:
                        continue  # skip other streams

                    if isinstance(event, ResponseReceived):
                        print(f"[{stream_id}] RESPONSE HEADERS:")
                        for k, v in event.headers:
                            print(f"{k.decode()}: {v.decode()}")
                    elif isinstance(event, DataReceived):
                        print(f"[{stream_id}] RESPONSE BODY:")
                        print(event.data.decode(errors="ignore"))
                    elif isinstance(event, StreamEnded):
                        stream_ended = True
                        print(f"[{stream_id}] Stream ended")
            else:
                print(f"[{stream_id}] No data received.")
                break
