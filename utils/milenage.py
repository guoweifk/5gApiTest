#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-18 10:11 
@file: milenage.py
@project: 5gAPItest
@describe: Powered By GW
"""

from dataclasses import dataclass
from Crypto.Cipher import AES
from utils.octet_string import OctetString # 确保 octet_string.py 存在并且包含 OctetString 类

@dataclass
class Milenage:
    op: bytes  # 16 字节 OP 值
    key: bytes  # 16 字节密钥
    rand: bytes
    opType: str

    res: OctetString = OctetString.from_spare(8)
    ck: OctetString = OctetString.from_spare(16)
    ik: OctetString = OctetString.from_spare(16)
    ak: OctetString = OctetString.from_spare(6)
    ak_r: OctetString = OctetString.from_spare(6)
    mac_a: OctetString = OctetString.from_spare(8)
    mac_s: OctetString = OctetString.from_spare(8)
    ck_ik: OctetString = OctetString.from_spare(32)  # CK || IK
    sqn: OctetString = OctetString.from_spare(6)  # SQN ⊕ AK

    def milenage_opc_gen(self) -> bytes:
        """生成 OPc 值 (AES-128 加密 + XOR 操作)"""
        if len(self.op) != 16 or len(self.key) != 16:
            raise ValueError("OP and key must be 16 bytes each")

        # 进行 AES-128 加密
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted_op = cipher.encrypt(self.op)

        # 逐字节 XOR 计算 OPc
        self.op = bytes(encrypted_op[i] ^ self.op[i] for i in range(16))
        return self.op

    def calculate_opc(self) -> bytes:
        """计算 OPc 并存储到实例"""
        opc_result = self.milenage_opc_gen()
        if not opc_result:
            raise RuntimeError("OPC calculation failed")
        return opc_result
