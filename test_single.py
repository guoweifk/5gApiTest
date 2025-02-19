#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-19 19:58 
@file: test_single.py
@project: 5gAPItest
@describe: Powered By GW
"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-10 10:39 
@file: apitest.py
@project: 5gAPItest
@describe: Powered By GW
"""
import socket
import sctp
import time
from function import authReceiveAndResult, securityReceiveAndResult,initContextAcceptReceiveAndResult


# 要发送的数据包
ngsetup_data = b"\x00\x15\x00\x3e\x00\x00\x04\x00\x1b\x00\x09\x00\x00\xf1\x10\x50" \
               b"\x00\x00\x00\x01\x00\x52\x40\x14\x08\x80\x55\x45\x52\x41\x4e\x53" \
               b"\x49\x4d\x2d\x67\x6e\x62\x2d\x31\x2d\x31\x2d\x31\x00\x66\x00\x0d" \
               b"\x00\x00\x00\x00\x01\x00\x00\xf1\x10\x00\x00\x00\x08\x00\x15\x40" \
               b"\x01\x40"

ini_data = data = b"\x00\x0f\x40\x48\x00\x00\x05\x00\x55\x00\x02\x00\x05\x00\x26\x00" \
                  b"\x1a\x19\x7e\x00\x41\x79\x00\x0d\x01\x00\xf1\x10\x00\x00\x00\x00" \
                  b"\x00\x00\x00\x00\x00\x2e\x04\xf0\xf0\xf0\xf0\x00\x79\x00\x13\x50" \
                  b"\x00\xf1\x10\x00\x00\x00\x01\x00\x00\xf1\x10\x00\x00\x01\xeb\x55" \
                  b"\x7a\xef\x00\x5a\x40\x01\x18\x00\x70\x40\x01\x00"


# 目标服务器
TARGET_IP = "127.0.0.5"
TARGET_PORT = 38412
wait_time = 0.1

# 单个线程执行的任务
def sctp_client_thread():
    # 为每个线程创建独立的 SCTP 套接字
    sk = sctp.sctpsocket_tcp(socket.AF_INET)
    sk.connect((TARGET_IP, TARGET_PORT))
    print(f" Connected and sending data...")

    sk.sendall(ngsetup_data)
    response_1 = sk.recv(1024)  # 接收返回数据
    print(f" Received ngsetup_Response: {response_1.hex()}")
    time.sleep(1)
    while True:
        # time.sleep(wait_time)
        sk.sendall(ini_data)

        # 接收、处理、发送auth相关信息
        auth_request = sk.recv(1024)  # 接收返回数据
        auth_response = authReceiveAndResult(auth_request.hex())
        # time.sleep(wait_time)
        sk.sendall(bytes.fromhex(auth_response))

        # 接收、处理、发送security相关信息
        security_request = sk.recv(1024)  # 接收返回数据
        security_response = securityReceiveAndResult(security_request.hex())
        # time.sleep(wait_time)
        sk.sendall(bytes.fromhex(security_response))
        # print(f"[Thread {thread_id}] Received security_response: {security_response}")


        # UEContext初始化消息
        init_context_accept_message = bytes(sk.recv(1024))  # 接收返回数据
        print(f"Received init_context_accept_message: {init_context_accept_message.hex()}")
        # print(f"Received init_context_accept_message : {init_context_accept_message.hex()}")
        # ue_response = initContextAcceptReceiveAndResult(init_context_accept_message)

sctp_client_thread()
