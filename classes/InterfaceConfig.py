#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-24 20:55 
@file: Config.py
@project: 5gAPItest
@describe: Powered By GW
"""

import socket
import netifaces


class InterfaceConfig:
    def __init__(self, ifname: str):
        # 获取接口名称（ifname） 并存储。
        self.ifname = ifname
        # 使用 socket.if_nametoindex() 获取接口索引（ifindex）
        self.ifindex = socket.if_nametoindex(self.ifname)
        # 网络接口名称和索引的映射表
        self.interfaces_map = self.get_network_interfaces_map()
        # num_ues：当前连接的 UE 数量。
        # prev：上一次的状态数据
        # config/state 相关变量：用于存储 配置信息 和 网络状态。
        # b 和 func：用于 回调函数 或 某些状态值。
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