#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-05-15 15:40 
@file: test_amf.py
@project: 5gAPItest
@describe: Powered By GW
"""
import sctp
import socket
while True:
    # 直接指定目的地址
    server_address = "192.168.55.78"
    server_port = 38412  # PFCP 默认端口

    # 创建 SCTP 套接字 (TCP-Style)
    sk = sctp.sctpsocket_tcp(socket.AF_INET)

    # 连接到目标地址和端口
    sk.connect((server_address, server_port))

    # 发送消息，ppid 是 Payload Protocol Identifier (这里示例设置为 60)
    sk.sctp_send(b"Hello!", ppid=socket.htonl(60))

    sk.close()
