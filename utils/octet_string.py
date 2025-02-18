#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-17 22:35 
@file: octet_string.py
@project: 5gAPItest
@describe: Powered By GW
"""
class OctetString:
    def __init__(self, value: bytes = b""):
        self.value = bytearray(value)  # 存储为可变的 bytearray

    def __repr__(self):
        return f"OctetString({self.value.hex()})"

    def length(self) -> int:
        """返回字节串的长度"""
        return len(self.value)

    @classmethod
    def from_spare(cls, length: int) -> 'OctetString':
        """生成指定长度的零填充字节串"""
        return cls(bytes(length))

    @staticmethod
    def concat(a: 'OctetString', b: 'OctetString') -> 'OctetString':
        """拼接两个 OctetString"""
        return OctetString(a.value + b.value)

    @staticmethod
    def xor(a: 'OctetString', b: 'OctetString') -> 'OctetString':
        """对两个 OctetString 进行逐字节 XOR"""
        # 判断传入的是 OctetString 对象还是 bytes 类型的对象
        a_value = a.value if isinstance(a, OctetString) else a
        b_value = b.value if isinstance(b, OctetString) else b

        return OctetString(bytes(x ^ y for x, y in zip(a_value, b_value)))

    def append_octet(self, v: int):
        """追加单个字节"""
        self.value.append(v & 0xFF)

    def append(self, v: "OctetString"):
        """追加另一个 OctetString 对象的数据"""
        self.value.extend(v.value)

    def append_octet2(self, v: int):
        """追加 2 字节整数 (big-endian)"""
        self.value.extend(v.to_bytes(2, byteorder="big"))

