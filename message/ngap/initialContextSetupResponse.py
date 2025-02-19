#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-19 15:25 
@file: initialContextSetupResponse.py
@project: 5gAPItest
@describe: Powered By GW
"""
from dataclasses import dataclass

@dataclass
class InitialContextSetupResponse:
    amf_ue_ngap_id: str
    ran_ue_ngap_id: str

    # 固定字段
    pdu_type: str = "20"  # Successful Outcome
    procedure_code: str = "0e"  # InitialContextSetup Procedure Code
    criticality: str = "000f"  # Criticality (reject)
    sequence_length: str = "000002"  # 固定为 2 个信息元素

    amf_ue_ngap_id_field: str = "000a"  # AMF-UE-NGAP-ID Identifier
    amf_ue_ngap_id_criticality: str = "40"  # Criticality (ignore)
    amf_ue_ngap_id_length: str = "02"  # Length of AMF-UE-NGAP-ID (2 bytes)

    ran_ue_ngap_id_field: str = "0055"  # RAN-UE-NGAP-ID Identifier
    ran_ue_ngap_id_criticality: str = "40"  # Criticality (ignore)
    ran_ue_ngap_id_length: str = "02"  # Length of RAN-UE-NGAP-ID (2 bytes)

    @classmethod
    def parse(cls, message: str) -> "InitialContextSetupResponse":
        """ 解析 InitialContextSetupResponse 消息 """
        message = message.upper()

        # 解析 NGAP PDU 头部
        pdu_type = message[0:2]  # "20" (Successful Outcome)
        procedure_code = message[2:4]  # "0e" (InitialContextSetup)
        criticality = message[4:8]  # "000f" (reject)
        sequence_length = message[8:14]  # "000002" (2 个信息元素)

        # 解析 AMF-UE-NGAP-ID
        amf_ue_ngap_id_field = message[14:18]  # "000a" (AMF-UE-NGAP-ID Identifier)
        amf_ue_ngap_id_criticality = message[18:20]  # "40" (ignore)
        amf_ue_ngap_id_length = int(message[20:22], 16)  # "02" (2 字节长度)
        amf_ue_ngap_id = message[22:22 + (amf_ue_ngap_id_length * 2)]  # "0002"（实际 ID）

        # 解析 RAN-UE-NGAP-ID
        ran_ue_ngap_id_field = message[22 + (amf_ue_ngap_id_length * 2):26 + (amf_ue_ngap_id_length * 2)]  # "0055"
        ran_ue_ngap_id_criticality = message[26 + (amf_ue_ngap_id_length * 2):28 + (amf_ue_ngap_id_length * 2)]  # "40"
        ran_ue_ngap_id_length = int(message[28 + (amf_ue_ngap_id_length * 2):30 + (amf_ue_ngap_id_length * 2)], 16)  # "02"
        ran_ue_ngap_id = message[30 + (amf_ue_ngap_id_length * 2):30 + (amf_ue_ngap_id_length * 2) + (ran_ue_ngap_id_length * 2)]  # "0001"

        return cls(
            amf_ue_ngap_id=amf_ue_ngap_id,
            ran_ue_ngap_id=ran_ue_ngap_id,
        )

    def to_hex(self) -> str:
        """ 将 InitialContextSetupResponse 结构体转换为原始十六进制消息 """
        return (
            f"{self.pdu_type}"
            f"{self.procedure_code}"
            f"{self.criticality}"
            f"{self.sequence_length}"
            f"{self.amf_ue_ngap_id_field}"
            f"{self.amf_ue_ngap_id_criticality}"
            f"{self.amf_ue_ngap_id_length}"
            f"{self.amf_ue_ngap_id}"
            f"{self.ran_ue_ngap_id_field}"
            f"{self.ran_ue_ngap_id_criticality}"
            f"{self.ran_ue_ngap_id_length}"
            f"{self.ran_ue_ngap_id}"
        ).upper()

    def __repr__(self):
        return (
            f"InitialContextSetupResponse(\n"
            f"  PDU Type: {self.pdu_type} (Successful Outcome)\n"
            f"  Procedure Code: {self.procedure_code} (InitialContextSetup)\n"
            f"  Criticality: {self.criticality} (reject)\n"
            f"  Message Length: {self.sequence_length}\n"
            f"  AMF-UE-NGAP-ID Field: {self.amf_ue_ngap_id_field}\n"
            f"  AMF-UE-NGAP-ID: {self.amf_ue_ngap_id}\n"
            f"  RAN-UE-NGAP-ID Field: {self.ran_ue_ngap_id_field}\n"
            f"  RAN-UE-NGAP-ID: {self.ran_ue_ngap_id}\n"
            f")"
        )
def test():
    # 示例数据
    message = "200e000f000002000a40020002005540020001"

    # 解析消息
    parsed_message = InitialContextSetupResponse.parse(message)
    print(parsed_message)

    # 生成回十六进制格式
    print("Hex Representation:", parsed_message.to_hex())

if __name__ == "__main__":
    test()