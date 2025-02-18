#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-18 15:42 
@file: authresponseMessage.py
@project: 5gAPItest
@describe: Powered By GW
"""
from dataclasses import dataclass


@dataclass
class AuthenticationResponseMessage:
    res_star: str
    nr_cgi: str
    plmn: str
    tac: str
    timestamp: str

    # **固定字段，直接初始化**
    protocol_discriminator: str = "7E"  # 固定 5G NAS
    security_header_type: str = "00"  # 无安全保护
    message_type: str = "57"  # Authentication Response
    element_id: str = "2D"  # 固定 Element ID
    response_len: str = "10"  # 固定 Response Length
    user_location_info_id: str = "0079"  # 固定 User Location Information ID
    criticality: str = "40"  # 固定 Criticality
    length: str = "13"  # 固定 User Location Information 长度

    @classmethod
    def parse(cls, message: str) -> "AuthenticationResponseMessage":
        """ 解析 Authentication Response 消息，包括 5G NAS 头部、RES* 和 User Location Information """
        message = message.upper()

        # 解析 5G NAS 头部
        protocol_discriminator = message[0:2]  # "7E" (5G NAS)
        security_header_type = message[2:4]  # "00" (无安全头)
        message_type = message[4:6]  # "57" (Authentication Response)
        element_id = message[6:8]
        response_len = message[8:10]
        # 解析 RES*（前 16 字节）
        res_star = message[10:42]  # 16 字节（32 个 hex 字符）

        # 解析 ID-UserLocationInformation
        user_location_info_id = message[42:46]  # "0079"

        # 解析 User Location Information
        criticality = message[46:48]  # "40" (固定值)
        length = message[48:50]  # "13" (User Location Information 长度)

        # 解析 NR-CGI（NR Cell Global Identity）
        nr_cgi = message[50:66]  # "50" (NR-CGI)

        plmn = message[66:74]  # "0000F110" (PLMN)
        # 解析 TAC（Tracking Area Code）
        tac = message[74:80]  # "000001" (TAC)

        # 解析时间戳
        timestamp = message[80:88]  # "EB5DA5BA" (TimeStamp)

        return cls(
            protocol_discriminator=protocol_discriminator,
            security_header_type=security_header_type,
            message_type=message_type,
            element_id=element_id,
            response_len=response_len,
            res_star=res_star,
            user_location_info_id=user_location_info_id,
            criticality=criticality,
            length=length,
            nr_cgi=nr_cgi,
            plmn=plmn,
            tac=tac,
            timestamp=timestamp
        )

    def to_hex(self) -> str:
        """ 将 AuthenticationResponseMessage 结构体转换回原始十六进制消息 """
        return (
            f"{self.protocol_discriminator}"
            f"{self.security_header_type}"
            f"{self.message_type}"
            f"{self.element_id}"
            f"{self.response_len}"
            f"{self.res_star}"
            f"{self.user_location_info_id}"
            f"{self.criticality}"
            f"{self.length}"
            f"{self.nr_cgi}"
            f"{self.plmn}"
            f"{self.tac}"
            f"{self.timestamp}"
        ).upper()

    def __repr__(self):
        return (
            f"AuthenticationResponseMessage(\n"
            f"  Protocol Discriminator: {self.protocol_discriminator} (固定)\n"
            f"  Security Header Type: {self.security_header_type} (固定)\n"
            f"  Message Type: {self.message_type} (固定)\n"
            f"  Element_id: {self.element_id} (固定)\n"
            f"  Response_len: {self.response_len} (固定)\n"
            f"  RES*: {self.res_star}\n"
            f"  ID-UserLocationInformation: {self.user_location_info_id} (固定)\n"
            f"  Criticality: {self.criticality} (固定)\n"
            f"  Length: {self.length}\n"
            f"  NR Cell Global Identity (NR-CGI): {self.nr_cgi}\n"
            f"  PLMN: {self.plmn}\n"
            f"  Tracking Area Code (TAC): {self.tac}\n"
            f"  TimeStamp: {self.timestamp}\n"
            f")"
        )


def test():
    # 示例数据
    auth_response_hex = "7e00572d106a9ef8fc9d2c11a36d4da18229c3b925007940135000f110000000010000f110000001eb5da5ba"

    # 解析 Authentication Response
    auth_response = AuthenticationResponseMessage.parse(auth_response_hex)

    # 打印解析结果
    print(auth_response)

    # 转换回原始十六进制消息
    reconstructed_hex = auth_response.to_hex()
    print(f"Reconstructed HEX: {reconstructed_hex}")


if __name__ == "__main__":
    test()
