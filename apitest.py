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
from threading import Thread


# 要发送的数据包
open5gs_ngsetup_data = b"\x00\x15\x00\x3e\x00\x00\x04\x00\x1b\x00\x09\x00\x00\xf1\x10\x50" \
               b"\x00\x00\x00\x01\x00\x52\x40\x14\x08\x80\x55\x45\x52\x41\x4e\x53" \
               b"\x49\x4d\x2d\x67\x6e\x62\x2d\x31\x2d\x31\x2d\x31\x00\x66\x00\x0d" \
               b"\x00\x00\x00\x00\x01\x00\x00\xf1\x10\x00\x00\x00\x08\x00\x15\x40" \
               b"\x01\x40"

free5gc_ngsetup_data = bytes.fromhex("00150041000004001b00090000f1105000000001005240140880554552414e53494d2d676e622d312d312d310066001000000000010000f110000010080102030015400140")
ngsetup_data = open5gs_ngsetup_data

open5gs_ini_data = b"\x00\x0f\x40\x48\x00\x00\x05\x00\x55\x00\x02\x00\x05\x00\x26\x00" \
                  b"\x1a\x19\x7e\x00\x41\x79\x00\x0d\x01\x00\xf1\x10\x00\x00\x00\x00" \
                  b"\x00\x00\x00\x00\x00\x2e\x04\xf0\xf0\xf0\xf0\x00\x79\x00\x13\x50" \
                  b"\x00\xf1\x10\x00\x00\x00\x01\x00\x00\xf1\x10\x00\x00\x01\xeb\x55" \
                  b"\x7a\xef\x00\x5a\x40\x01\x18\x00\x70\x40\x01\x00"

free5gc_ini_data = bytes.fromhex("000f40480000050055000200010026001a197e004179000d0100f1100000000000000000102e04f0f0f0f0007900135000f110000000010000f110000001eb617019005a4001180070400100")
ini_data =  open5gs_ini_data


# 目标服务器
TARGET_IP = "127.0.0.5"
TARGET_PORT = 38412
wait_time_start =0.1
wait_time_end = 10

# 单个线程执行的任务
def sctp_client_thread(thread_id):
    # 为每个线程创建独立的 SCTP 套接字
    time.sleep(random.uniform(0.1, 0.2))
    sk = sctp.sctpsocket_tcp(socket.AF_INET)
    try:
        sk.connect((TARGET_IP, TARGET_PORT))
        print(f"[Thread {thread_id}] Connected and sending data...")

        sk.sendall(ngsetup_data)
        response_1 = sk.recv(1024)  # 接收返回数据
        # print(f"[Thread {thread_id}] Received ngsetup_Response: {response_1.hex()}")
        time.sleep(1)
        sk.sendall(ini_data)
        while True:
            # time.sleep(wait_time)
            # sk.recv(1024)


            # 接收、处理、发送auth相关信息
            auth_request = sk.recv(1024)  # 接收返回数据
            # print(f"[Thread {thread_id}] Received auth_request: {auth_request.hex()}")
            auth_response = authReceiveAndResult(auth_request.hex())
            # time.sleep(wait_time)
            # time.sleep(random.uniform(1.1, 1.5))
            sk.sendall(bytes.fromhex(auth_response))

            # 接收、处理、发送security相关信息
            security_request = sk.recv(1024)  # 接收返回数据
            # print(f"[Thread {thread_id}] Received security_request: {security_request.hex()}")
            security_response = securityReceiveAndResult(security_request.hex())
            # time.sleep(wait_time)
            sk.sendall(bytes.fromhex(security_response))
            # print(f"[Thread {thread_id}] Received security_response: {security_response}")
            # time.sleep(wait_time)


            # UEContext初始化消息
            init_context_accept_message = bytes(sk.recv(1024))  # 接收返回数据
            # print(f"[Thread {thread_id}] Received init_context_accept_message: {init_context_accept_message.hex()}")
            # print(f"Received init_context_accept_message : {init_context_accept_message.hex()}")
            # ue_response = initContextAcceptReceiveAndResult(init_context_accept_message)

            sk.sendall(ini_data)
            sk.recv(1024)
            # print(1)
            # time.sleep(random.uniform(0.1, 1))


    except KeyboardInterrupt:
        print(f"[Thread {thread_id}] Terminating.")
    except Exception as e:
        print(f"[Thread {thread_id}] Error: {e}")
    finally:
        sk.close()  # 确保套接字在线程结束时关闭
        print(f"[Thread {thread_id}] Connection closed.")




def test_mulit():
    # sctp_client_thread(1)
    # 255 个线程直接会让AMF崩溃报错
    num_threads = 1
    threads = []

    for i in range(num_threads):
        t = Thread(target=sctp_client_thread, args=(i,))
        t.start()
        threads.append(t)

    # 等待所有线程完成
    for t in threads:
        t.join()


def test_one():
    time.sleep(random.uniform(0.1, 0.2))
    sk = sctp.sctpsocket_tcp(socket.AF_INET)
    sk.connect((TARGET_IP, TARGET_PORT))
    print(f" Connected and sending data...")
    sk.sendall(ngsetup_data)
    response_1 = sk.recv(1024)  # 接收返回数据
    time.sleep(1)
    sk.sendall(ini_data)
    # time.sleep(wait_time)
    # sk.recv(1024)
    # 接收、处理、发送auth相关信息
    auth_request = sk.recv(1024)  # 接收返回数据
    # print(f"[Thread {thread_id}] Received auth_request: {auth_request.hex()}")
    auth_response = authReceiveAndResult(auth_request.hex())
    # time.sleep(wait_time)
    # time.sleep(random.uniform(1.1, 1.5))
    sk.sendall(bytes.fromhex(auth_response))
    # 接收、处理、发送security相关信息
    security_request = sk.recv(1024)  # 接收返回数据
    # print(f"[Thread {thread_id}] Received security_request: {security_request.hex()}")
    security_response = securityReceiveAndResult(security_request.hex())
    # time.sleep(wait_time)
    sk.sendall(bytes.fromhex(security_response))
    # print(f"[Thread {thread_id}] Received security_response: {security_response}")
    # time.sleep(wait_time)

    # UEContext初始化消息
    init_context_accept_message = bytes(sk.recv(1024))  # 接收返回数据
    print(f"Received init_context_accept_message: {init_context_accept_message.hex()}")
    ue_response = initContextAcceptReceiveAndResult(init_context_accept_message)

    sk.sendall(ini_data)
    sk.recv(1024)
    # print(1)
    # time.sleep(random.uniform(0.1, 1))

if __name__ == "__main__":
    # test_mulit()
    test_one()