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
import random
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

ue_release = b"\x20\x29\x00\x26\x00\x00\x03\x00\x0a\x40\x02\x00\x01\x00\x55\x40\x02\x00\x04\x00\x79\x40\x13\x50\x00\xf1\x10\x00\x00\x00\x01\x00\x00\xf1\x10\x00\x00\x01\xeb\x55\x7a\xef"
init_release = b"\x20\x0e\x00\x0f\x00\x00\x02\x00\x0a\x40\x02\x00\x02\x00\x55\x40\x02\x00\x05"
PDU_establish = b"\x00\x2e\x40\x5e\x00\x00\x04\x00\x0a\x00\x02\x00\x02\x00\x55\x00\x02\x00\x05\x00\x26\x00\x34\x33\x7e\x02\x7c\xcd\x77\x64\x02\x7e\x00\x67\x01\x00\x15\x2e\x01\x01\xc1\xff\xff\x91\xa1\x28\x01\x00\x7b\x00\x07\x80\x00\x0a\x00\x00\x0d\x00\x12\x01\x81\x22\x01\x01\x25\x09\x08\x69\x6e\x74\x65\x72\x6e\x65\x74\x00\x79\x40\x13\x50\x00\xf1\x10\x00\x00\x00\x01\x00\x00\xf1\x10\x00\x00\x01\xeb\x55\x7a\xef"

PDU_reponse = b"\x20\x1d\x00\x3b\x00\x00\x04\x00\x0a\x40\x02\x00\x02\x00\x55\x40\x02\x00\x05" \
              b"\x00\x4b\x40\x11\x00\x00\x01\x0d\x00\x03\xe0\x7f\x00\x00\x01\x00\x00\x00\x03" \
              b"\x00\x01\x00\x79\x40\x13\x50\x00\xf1\x10\x00\x00\x00\x01\x00\x00\xf1\x10\x00" \
              b"\x00\x01\xeb\x55\x7a\xef"

# 目标服务器
TARGET_IP = "127.0.0.5"
TARGET_PORT = 38412


# def authenResCalculate():


# 单个线程执行的任务
def sctp_client_thread(thread_id):
    sk = sctp.sctpsocket_tcp(socket.AF_INET)
    sk.connect((TARGET_IP, TARGET_PORT))

    print(f"[Thread {thread_id}] Connected and sending data...")

    ngsetup_Response = sk.sendall(ngsetup_data)
    response_1 = sk.recv(1024)  # 接收返回数据
    # print(f"Received ngsetup_Response : {ngsetup_Response}")
    time.sleep(1)
    # try:
    #     while True:

    time.sleep(random.uniform(0.1, 0.5))
    sk.sendall(ini_data)

    # 接收、处理、发送auth相关信息
    auth_request = bytes(sk.recv(1024))  # 接收返回数据
    print(auth_request.hex())
    auth_response = authReceiveAndResult(auth_request.hex())
    time.sleep(random.uniform(0.1, 0.5))
    sk.sendall(bytes.fromhex(auth_response))
    # 接收、处理、发送security相关信息
    security_request = sk.recv(1024)  # 接收返回数据
    security_response = securityReceiveAndResult(security_request.hex())
    time.sleep(random.uniform(0.1, 0.5))
    sk.sendall(bytes.fromhex(security_response))
    time.sleep(random.uniform(0.1, 0.5))

    # UEContext初始化消息
    init_context_setup_request = bytes(sk.recv(1024))  # 接收返回数据
    print(f"Received init_context_setup_request : {init_context_setup_request.hex()}")
    ue_response = initContextAcceptReceiveAndResult(init_context_setup_request)

    sk.sendall(ue_response)
    time.sleep(random.uniform(0.1, 0.5))
    sk.sendall(init_release)
    time.sleep(random.uniform(0.1, 0.5))
    sk.sendall(PDU_establish)
    time.sleep(random.uniform(0.1, 0.5))
    sk.sendall(PDU_reponse)
    # sk.close()
    print(f"[Thread {thread_id}] Connection closed.")
    time.sleep(random.uniform(0, 1))


# except KeyboardInterrupt:
#     print(f"[Thread {thread_id}] Terminating.")
# except Exception as e:
#     print(f"[Thread {thread_id}] Error: {e}")


sctp_client_thread(1)

# for i in range(num_threads):
#     t = Thread(target=sctp_client_thread, args=(i,))
#     t.start()
#     threads.append(t)
#
# # 等待所有线程完成
# for t in threads:
#     t.join()
