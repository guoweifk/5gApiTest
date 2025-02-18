#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-16 19:48 
@file: ngapSetup.py
@project: 5gAPItest
@describe: Powered By GW
"""
import struct

class NGSetupRequest:
    def __init__(self, raw_data: bytes):
        self.raw_data = raw_data
        self.message_type = None
        self.length = None
        self.plmn_id = None
        self.gnb_id = None
        self.gnb_name = None
        self.tai_list = []

        self.parse()

    def parse_plmn(self, plmn_bytes):
        """ 将 PLMN ID 字节转换为 MCC/MNC 字符串 """
        if len(plmn_bytes) != 3:
            return "Invalid PLMN"
        mcc = f"{plmn_bytes[0]:X}{(plmn_bytes[1] & 0xF0) >> 4:X}{plmn_bytes[1] & 0x0F:X}"
        mnc = f"{(plmn_bytes[2] & 0xF0) >> 4:X}{plmn_bytes[2] & 0x0F:X}" if (plmn_bytes[1] & 0xF0) != 0xF0 else f"{plmn_bytes[2]:X}"
        return f"{mcc}/{mnc}"

    def parse(self):
        """ 解析 NGSetupRequest 消息 """
        try:
            offset = 0

            # 解析 PDU Type (InitiatingMessage)
            self.message_type = struct.unpack_from("!H", self.raw_data, offset)[0]
            offset += 2

            # 解析消息长度
            self.length = struct.unpack_from("!H", self.raw_data, offset)[0]
            offset += 2

            # 解析 Global RAN Node ID (IE ID)
            ie_id = struct.unpack_from("!H", self.raw_data, offset)[0]
            offset += 2
            if ie_id == 0x001B:  # GlobalRANNodeID
                ie_length = struct.unpack_from("!H", self.raw_data, offset)[0]
                offset += 2
                self.plmn_id = self.parse_plmn(self.raw_data[offset:offset+3])  # 解析 PLMN ID
                offset += 3
                self.gnb_id = struct.unpack_from("!I", b"\x00" + self.raw_data[offset:offset+3])[0]  # gNB ID (24-bit)
                offset += 3

            # 解析 gNB Name (IE ID)
            ie_id = struct.unpack_from("!H", self.raw_data, offset)[0]
            offset += 2
            if ie_id == 0x0052:  # gNB Name
                ie_length = struct.unpack_from("!H", self.raw_data, offset)[0]
                offset += 2
                self.gnb_name = self.raw_data[offset:offset+ie_length].decode("utf-8").strip("\x00")
                offset += ie_length

            # 解析 TAI List (IE ID)
            ie_id = struct.unpack_from("!H", self.raw_data, offset)[0]
            offset += 2
            if ie_id == 0x0066:  # Supported TAI List
                ie_length = struct.unpack_from("!H", self.raw_data, offset)[0]
                offset += 2
                plmn_id = self.parse_plmn(self.raw_data[offset:offset+3])  # 解析 PLMN ID
                offset += 3
                tac = struct.unpack_from("!I", b"\x00" + self.raw_data[offset:offset+3])[0]  # TAC (24-bit)
                offset += 3
                self.tai_list.append({"PLMN": plmn_id, "TAC": tac})

        except Exception as e:
            print(f"解析错误: {e}")

    def display(self):
        """ 打印解析后的 NGSetupRequest 信息 """
        print("=== NGSetupRequest 解析结果 ===")
        print(f"消息类型: {self.message_type}")
        print(f"消息长度: {self.length}")
        print(f"PLMN ID: {self.plmn_id}")
        print(f"gNB ID: {self.gnb_id}")
        print(f"gNB 名称: {self.gnb_name}")
        print(f"支持的 TAI 列表: {self.tai_list}")

# 测试代码
ngsetup_data = b"\x00\x15\x00\x3e\x00\x00\x04\x00\x1b\x00\x09\x00\x00\xf1\x10\x50" \
               b"\x00\x00\x00\x01\x00\x52\x40\x14\x08\x80\x55\x45\x52\x41\x4e\x53" \
               b"\x49\x4d\x2d\x67\x6e\x62\x2d\x31\x2d\x31\x2d\x31\x00\x66\x00\x0d" \
               b"\x00\x00\x00\x00\x01\x00\x00\xf1\x10\x00\x00\x00\x08\x00\x15\x40" \
               b"\x01\x40"

ng_setup = NGSetupRequest(ngsetup_data)
ng_setup.display()

