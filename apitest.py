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
from threading import Thread
import random
from function import authReceive_Result

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



security_response = b"\x00\x2e\x40\x67\x00\x00\x04\x00\x0a\x00\x02\x00\x02\x00\x55\x00\x02\x00\x05\x00\x26\x00\x3d\x3c\x7e\x04\x03\x5c\x8c\x23\x00\x7e\x00\x5e\x77\x00\x09\x45\x73\x80\x61\x21\x85\x61\x51\xf1\x71\x00\x23\x7e\x00\x41\x79\x00\x0d\x01\x00\xf1\x10\x00\x00\x00\x00\x00\x00\x00\x00\x10\x01\x00\x2e\x04\xf0\xf0\xf0\xf0\x2f\x02\x01\x01\x53\x01\x00\x00\x79\x40\x13\x50\x00\xf1\x10\x00\x00\x00\x01\x00\x00\xf1\x10\x00\x00\x01\xeb\x55\x7a\xef"
ue_release=b"\x20\x29\x00\x26\x00\x00\x03\x00\x0a\x40\x02\x00\x01\x00\x55\x40\x02\x00\x04\x00\x79\x40\x13\x50\x00\xf1\x10\x00\x00\x00\x01\x00\x00\xf1\x10\x00\x00\x01\xeb\x55\x7a\xef"
init_release=b"\x20\x0e\x00\x0f\x00\x00\x02\x00\x0a\x40\x02\x00\x02\x00\x55\x40\x02\x00\x05"
PDU_establish=b"\x00\x2e\x40\x5e\x00\x00\x04\x00\x0a\x00\x02\x00\x02\x00\x55\x00\x02\x00\x05\x00\x26\x00\x34\x33\x7e\x02\x7c\xcd\x77\x64\x02\x7e\x00\x67\x01\x00\x15\x2e\x01\x01\xc1\xff\xff\x91\xa1\x28\x01\x00\x7b\x00\x07\x80\x00\x0a\x00\x00\x0d\x00\x12\x01\x81\x22\x01\x01\x25\x09\x08\x69\x6e\x74\x65\x72\x6e\x65\x74\x00\x79\x40\x13\x50\x00\xf1\x10\x00\x00\x00\x01\x00\x00\xf1\x10\x00\x00\x01\xeb\x55\x7a\xef"

PDU_reponse= b"\x20\x1d\x00\x3b\x00\x00\x04\x00\x0a\x40\x02\x00\x02\x00\x55\x40\x02\x00\x05" \
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

    sk.sendall(ngsetup_data)
    response_1 = sk.recv(1024)  # 接收返回数据
    print(f"[Thread {thread_id}] Received response 1: {response_1.hex()}")
    time.sleep(1)
    try:
        while True:

            time.sleep(random.uniform(0.1,0.5))
            sk.sendall(ini_data)

            auth_request = sk.recv(1024)  # 接收返回数据
            auth_response = authReceive_Result(auth_request)
            # print(f"[Thread {thread_id}] Received response : {response_1.hex()}")
            #
            #
            # ngap_id_offset = 22
            # ngap_id_length = 4
            # ngap_id = response_1.hex()[ngap_id_offset:ngap_id_offset + ngap_id_length]
            #
            #
            # print(f"[Thread {thread_id}] Received response 1: {response_1.hex()}")
            # ngap_id_bytes = bytes.fromhex(ngap_id)
            #
            #
            # print(f"[Thread {thread_id}] Received response 1: {ngap_id}")
            # auth_response = (b"\x00\x2e\x40\x40\x00\x00\x04\x00\x0a\x00\x02"+
            #                         ngap_id_bytes +
            #                         b"\x00\x55\x00\x02\x00\x05\x00\x26\x00\x16\x15\x7e\x00\x57\x2d\x10\x18\xd0\xc2\xa3\x37\x0f\x62\x90\x54\xf9\x51\xfc\x85\x8b\x92\xf7\x00\x79\x40\x13\x50\x00\xf1\x10\x00\x00\x00\x01\x00\x00\xf1\x10\x00\x00\x01
            #                         \xeb\x55\x7a\xef"
            #                         )

            time.sleep(random.uniform(0.1,0.5))
            sk.sendall(auth_response)
            print(auth_response)
            response_2 = sk.recv(1024)  # 接收返回数据
            print(f"[Thread {thread_id}] Received response 2: {response_2.hex()}")
            time.sleep(random.uniform(0.1,0.5))
            sk.sendall(security_response)
            time.sleep(random.uniform(0.1,0.5))
            sk.sendall(ue_release)
            time.sleep(random.uniform(0.1,0.5))
            sk.sendall(init_release)
            time.sleep(random.uniform(0.1,0.5))
            sk.sendall(PDU_establish)
            time.sleep(random.uniform(0.1,0.5))
            sk.sendall(PDU_reponse)
            # sk.close()
            print(f"[Thread {thread_id}] Connection closed.")
            time.sleep(random.uniform(0,1))
    except KeyboardInterrupt:
        print(f"[Thread {thread_id}] Terminating.")
    except Exception as e:
        print(f"[Thread {thread_id}] Error: {e}")

# 启动并发的3个线程
threads = []
num_threads =1
sctp_client_thread(1)


# for i in range(num_threads):
#     t = Thread(target=sctp_client_thread, args=(i,))
#     t.start()
#     threads.append(t)
#
# # 等待所有线程完成
# for t in threads:
#     t.join()
