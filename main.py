#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-10 10:39
@file: apitest.py
@project: 5gAPItest
@describe: Powered By GW
"""

#  todo: 日志、保存文件

import sys, sctp, socket,struct

open5gs_ngsetup_data = b"\x00\x15\x00\x3e\x00\x00\x04\x00\x1b\x00\x09\x00\x00\xf1\x10\x50" \
               b"\x00\x00\x00\x01\x00\x52\x40\x14\x08\x80\x55\x45\x52\x41\x4e\x53" \
               b"\x49\x4d\x2d\x67\x6e\x62\x2d\x31\x2d\x31\x2d\x31\x00\x66\x00\x0d" \
               b"\x00\x00\x00\x00\x01\x00\x00\xf1\x10\x00\x00\x00\x08\x00\x15\x40" \
               b"\x01\x40"
#
# if len(sys.argv) != 2:
#   print("Usage: free5gc.py server-address")
#   exit(0)
print ("1")
sk = sctp.sctpsocket_tcp(socket.AF_INET)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
print ("2")
sk.connect(("192.168.123.165", 38412))
print ("33")
# sk.sendall(open5gs_ngsetup_data)
sk.sctp_send(b"Hello!", ppid=socket.htonl(60))


# response_1 = sk.recv(1024)
# print (response_1)
# sk.close()