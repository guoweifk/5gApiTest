#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-18 19:43 
@file: ngapDownLinkNASTransport.py
@project: 5gAPItest
@describe: Powered By GW
"""
from dataclasses import dataclass


@dataclass
class NGAPDownLinkTransportNASMessage:
    message_length: str
    amf_ue_ngap_id: str
    ran_ue_ngap_id: str
    nas_pdu_length: str


    # **固定字段**
    pdu_type: str = "0004"  # 固定 NGAP PDU Type
    procedure_code: str = "403E"  # 固定 Downlink NAS Transport Procedure Code
    criticality: str = "00"  # 固定 Criticality
    amf_ue_ngap_id_field: str = "000A"  # 固定 AMF-UE-NGAP-ID Identifier
    amf_ue_ngap_id_length: str = "0002"
    ran_ue_ngap_id_field: str = "0055"  # 固定 RAN-UE-NGAP-ID Identifier
    ran_ue_ngap_id_length: str = "0002"
    nas_pdu_field: str = "0026002b"  # 固定 NAS-PDU Identifier


    @classmethod
    def parse(cls, message: str) -> "NGAPDownLinkTransportNASMessage":
        """ 解析 NGAP Downlink NAS Transport 消息（包含所有字段） """
        message = message.upper()

        # 解析 NGAP 头部
        pdu_type = message[0:4]  # "0004" (固定)
        procedure_code = message[4:8]  # "403E" (固定)
        criticality = message[8:10]  # "00" (固定)
        message_length = message[10:14]  # 变换的消息长度

        # 解析 AMF-UE-NGAP-ID
        amf_ue_ngap_id_field = message[14:18]  # "000A" (固定)
        amf_ue_ngap_id_length = int(message[18:22], 16)  # "0002"
        amf_ue_ngap_id = message[22:22 + (amf_ue_ngap_id_length * 2)]  # "0002"（变换）

        # 解析 RAN-UE-NGAP-ID
        ran_ue_ngap_id_field = message[22 + (amf_ue_ngap_id_length * 2):26 + (amf_ue_ngap_id_length * 2)]  # "0055" (固定)
        ran_ue_ngap_id_length = int(message[26 + (amf_ue_ngap_id_length * 2):30 + (amf_ue_ngap_id_length * 2)],
                                    16)  # "0002"
        ran_ue_ngap_id = message[30 + (amf_ue_ngap_id_length * 2):30 + (amf_ue_ngap_id_length * 2) + (
                ran_ue_ngap_id_length * 2)]  # "0001"（变换）

        # 解析 NAS-PDU
        nas_pdu_field = message[30 + (amf_ue_ngap_id_length * 2) + (ran_ue_ngap_id_length * 2):38 + (
                amf_ue_ngap_id_length * 2) + (ran_ue_ngap_id_length * 2)]  # "0026" (固定)
        nas_pdu_length = message[38 + (amf_ue_ngap_id_length * 2) + (ran_ue_ngap_id_length * 2):]  # 变换的 NAS-PDU 内容

        return cls(
            message_length=message_length,
            amf_ue_ngap_id=amf_ue_ngap_id,
            ran_ue_ngap_id=ran_ue_ngap_id,
            nas_pdu_length=nas_pdu_length,
        )

    def to_hex(self) -> str:
        """ 将 NGAPDownLinkTransportNASMessage 结构体转换回原始十六进制消息 """
        return (
            f"{self.pdu_type}"
            f"{self.procedure_code}"
            f"{self.criticality}"
            f"{self.message_length}"
            f"{self.amf_ue_ngap_id_field}"
            f"{len(self.amf_ue_ngap_id) // 2:04X}"
            f"{self.amf_ue_ngap_id}"
            f"{self.ran_ue_ngap_id_field}"
            f"{len(self.ran_ue_ngap_id) // 2:04X}"
            f"{self.ran_ue_ngap_id}"
            f"{self.nas_pdu_field}"
            f"{self.nas_pdu_length}"
        ).upper()

    def __repr__(self):
        return (
            f"NGAPDownLinkTransportNASMessage(\n"
            f"  PDU Type: {self.pdu_type} (固定)\n"
            f"  Procedure Code: {self.procedure_code} (固定)\n"
            f"  Criticality: {self.criticality} (固定)\n"
            f"  Message_length: {self.message_length} \n"
            f"  AMF-UE-NGAP-ID Field: {self.amf_ue_ngap_id_field} (固定)\n"
            f"  AMF-UE-NGAP-ID: {self.amf_ue_ngap_id}\n"
            f"  RAN-UE-NGAP-ID Field: {self.ran_ue_ngap_id_field} (固定)\n"
            f"  RAN-UE-NGAP-ID: {self.ran_ue_ngap_id}\n"
            f"  NAS-PDU Field: {self.nas_pdu_field} (固定)\n"
            f"  NAS-PDU Length: {self.nas_pdu_length} bytes\n"
            f")"
        )


def test():
    # 示例数据（不包含 NAS-PDU）
    ngap_message_hex = "0004403E000003000A000200020055000200010026002B2A"
    # 解析 NGAP Downlink NAS Transport
    ngap_downlink = NGAPDownLinkTransportNASMessage.parse(ngap_message_hex)

    # 打印解析结果
    print(ngap_downlink)

    # 转换回原始十六进制消息
    original_hex = ngap_downlink.to_hex()
    print(f"Reconstructed HEX: {original_hex}")


if __name__ == "__main__":
    test()
