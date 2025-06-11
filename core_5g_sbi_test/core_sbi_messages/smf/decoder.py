#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-04-25 18:08 
@file: decoder.py
@project: 5gAPItest
@describe: Powered By GW
"""
from scapy.all import IP, TCP, send

src_ip = "127.0.0.200"
dst_ip = "127.0.0.13"
src_port = 7777
dst_port = 7777

# 构造 TCP SYN 包（伪造源地址和端口）
ip = IP(src=src_ip, dst=dst_ip)
syn = TCP(sport=src_port, dport=dst_port, flags='S', seq=1000)

pkt = ip/syn

# 发包
send(pkt)
