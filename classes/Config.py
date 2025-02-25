#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-24 20:55 
@file: Config.py
@project: 5gAPItest
@describe: Powered By GW
"""
import ctypes
import time
import socket
import ipaddress
import os
import netifaces


class Config:
    def __init__(self, ifname: str):
        self.ifname = ifname
        self.ifindex = socket.if_nametoindex(self.ifname)
        self.interfaces_map = self.get_network_interfaces_map()
        self.num_ues = 0
        self.prev = 0
        self.config = None
        self.state = None
        self.state_map = None
        self.config_map = None
        self.b = None
        self.func = None
        # self.load()
        self.previous_data = {}

    @staticmethod
    def get_network_interfaces_map():
        interface_map = {}
        interfaces = netifaces.interfaces()  # Get interface names using netifaces

        for interface_name in interfaces:
            try:
                if_index = socket.if_nametoindex(interface_name)
                interface_map[if_index] = interface_name
            except OSError:
                print(f"Error retrieving if_index for interface: {interface_name}")

        return interface_map