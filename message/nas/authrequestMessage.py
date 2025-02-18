#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-18 19:19 
@file: authrequestMessage.py
@project: 5gAPItest
@describe: Powered By GW
"""
from dataclasses import dataclass

@dataclass
class AuthenticationRequestMessage:
    protocol_discriminator: str
    security_header_type: str
    message_type: str
    ngKSI_tsc: str
    ngKSI_ksi: str
    abba_length: int
    abba_value: str
    rand_element_id: str
    rand: str
    autn_element_id: str
    autn_length: int
    sqn_xor_ak: str
    amf: str
    mac: str

    @classmethod
    def parse(cls, message: str) -> "AuthenticationRequestMessage":
        """ 解析 Authentication Request 消息 """
        # 将消息转换为大写，确保统一格式
        message = message.upper()

        # 解析 5G NAS 头部
        protocol_discriminator = message[0:2]  # "7E"
        security_header_type = message[2:4]  # "00"
        message_type = message[4:6]  # "56"

        # 解析 NAS Key Set Identifier (ngKSI)
        ngKSI_byte = int(message[6:8], 16)
        ngKSI_tsc = str((ngKSI_byte & 0b10000000) >> 7)  # 最高位是 TSC
        ngKSI_ksi = str(ngKSI_byte & 0b00000111)  # 低三位是 KSI

        # 解析 ABBA
        abba_length = int(message[8:10], 16)  # 长度字段
        abba_value = message[10:10 + (abba_length * 2)]  # ABBA 值

        # 解析 Authentication Parameter RAND
        rand_start = 10 + (abba_length * 2)
        rand_element_id = message[rand_start:rand_start + 2]  # "21"
        rand = message[rand_start + 2:rand_start + 34]  # 16字节 RAND

        # 解析 Authentication Parameter AUTN
        autn_start = rand_start + 34
        autn_element_id = message[autn_start:autn_start + 2]  # "20"
        autn_length = int(message[autn_start + 2:autn_start + 4], 16)  # "10"

        # 解析 SQN_xor_AK (6字节)
        sqn_xor_ak_start = autn_start + 4
        sqn_xor_ak = message[sqn_xor_ak_start:sqn_xor_ak_start + 12]  # 6字节 = 12个十六进制字符

        # 解析 AMF (2字节)
        amf_start = sqn_xor_ak_start + 12
        amf = message[amf_start:amf_start + 4]  # 2字节 = 4个十六进制字符

        # 解析 MAC (8字节)
        mac_start = amf_start + 4
        mac = message[mac_start:mac_start + 20]  # 8字节 = 20个十六进制字符

        # 返回解析后的对象
        return cls(
            protocol_discriminator=protocol_discriminator,
            security_header_type=security_header_type,
            message_type=message_type,
            ngKSI_tsc=ngKSI_tsc,
            ngKSI_ksi=ngKSI_ksi,
            abba_length=abba_length,
            abba_value=abba_value,
            rand_element_id=rand_element_id,
            rand=rand,
            autn_element_id=autn_element_id,
            autn_length=autn_length,
            sqn_xor_ak=sqn_xor_ak,
            amf=amf,
            mac=mac
        )

    def __repr__(self):
        """ 以易读的格式显示解析结果 """
        return (
            f"AuthenticationRequest(\n"
            f"  Protocol Discriminator: {self.protocol_discriminator}\n"
            f"  Security Header Type: {self.security_header_type}\n"
            f"  Message Type: {self.message_type}\n"
            f"  NAS Key Set Identifier:\n"
            f"    - TSC: {self.ngKSI_tsc} (0 = Native, 1 = Mapped)\n"
            f"    - KSI: {self.ngKSI_ksi}\n"
            f"  ABBA:\n"
            f"    - Length: {self.abba_length}\n"
            f"    - Value: {self.abba_value}\n"
            f"  Authentication Parameters:\n"
            f"    - RAND Element ID: {self.rand_element_id}\n"
            f"    - RAND: {self.rand}\n"
            f"    - AUTN:\n"
            f"      - Element ID: {self.autn_element_id}\n"
            f"      - Length: {self.autn_length}\n"
            f"      - SQN_xor_AK: {self.sqn_xor_ak}\n"
            f"      - AMF: {self.amf}\n"
            f"      - MAC: {self.mac}\n"
            f")"
        )

def test():

    # 示例数据
    auth_request_hex = "7E005601020000216B0BBF58144C8D74ADE24B5626BD5D2F2010719762A4686F80005EC4E5F58C90A2040000"

    # 解析 Authentication Request 消息
    auth_request = AuthenticationRequestMessage.parse(auth_request_hex)

    # 打印解析结果
    print(auth_request)

if __name__ == "__main__":
    test()
