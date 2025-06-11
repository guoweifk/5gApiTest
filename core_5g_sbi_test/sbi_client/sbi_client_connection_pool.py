#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-04 16:38 
@file: sbi_client_connection_pools.py
@project: 5gAPItest
@describe: Powered By GW
"""
from core_5g_sbi_test.sbi_client.sbi_client_connection import SBIConnection


class SBIConnectionPool:
    def __init__(self):
        self.connections = {}  # {(host, port): SBIConnection}

    def get_connection(self, host, port):
        key = (host, port)
        if key not in self.connections:
            self.connections[key] = SBIConnection(host, port)
        return self.connections[key]

    def close_all(self):
        for conn in self.connections.values():
            conn.close()
        self.connections.clear()
