#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-18 20:50 
@file: ngapUpLinkNASTransport.py
@project: 5gAPItest
@describe: Powered By GW
"""
from dataclasses import dataclass

@dataclass
class NGAPUplinkTransportNASMessage:

    ngap_message_len: str
    amf_ue_ngap_id: str
    ran_ue_ngap_id: str
    nas_pdu_type: str
    nas_pdu_length: str

    # **固定字段，初始化时写死**
    pdu_type: str = "002E"  # 固定 NGAP PDU Type
    procedure_code: str = "40"  # 固定 Uplink NAS Transport Procedure Code
    extension: str = "00"  # 固定 Criticality
    squence_length: str = "0004" # 固定 squence_length
    amf_ue_ngap_id_field: str = "000A"  # 固定 AMF-UE-NGAP-ID Identifier
    amf_ue_ngap_id_type_len: str = "0002"
    ran_ue_ngap_id_field: str = "0055"  # 固定 RAN-UE-NGAP-ID Identifier
    ran_ue_ngap_id_type_len: str = "0002"
    nas_pdu_field: str = "0026"  # 固定 NAS-PDU Identifier

    @classmethod
    def parse(cls, message: str) -> "NGAPUplinkTransportNASMessage":
        """ 解析 Uplink NAS Transport 消息（仅解析变换字段） """
        message = message.upper()

        ngap_message_len = message[6:8]
        # 解析 AMF-UE-NGAP-ID
        amf_ue_ngap_id_type = message[18:22]  # "0002"
        amf_ue_ngap_id = message[22:26]  # 变化的 ID

        # 解析 RAN-UE-NGAP-ID
        ran_ue_ngap_id_type = message[30:34]  # "0002"
        ran_ue_ngap_id = message[34:38]  # 变化的 ID

        # 解析 NAS-PDU
        nas_pdu_type = message[42:46]  # 变化的 Type
        nas_pdu_length = message[46:48]  # 变化的 Length

        return cls(
            ngap_message_len = ngap_message_len,
            amf_ue_ngap_id_type_len=amf_ue_ngap_id_type,
            amf_ue_ngap_id=amf_ue_ngap_id,
            ran_ue_ngap_id_type_len=ran_ue_ngap_id_type,
            ran_ue_ngap_id=ran_ue_ngap_id,
            nas_pdu_type=nas_pdu_type,
            nas_pdu_length=nas_pdu_length
        )

    def to_hex(self) -> str:
        """ 将 UplinkNASTransport 结构体转换回原始十六进制消息 """
        return (
            f"{self.pdu_type}"
            f"{self.procedure_code}"
            f"{self.ngap_message_len}"
            f"{self.extension}"
            f"{self.squence_length}"
            f"{self.amf_ue_ngap_id_field}"
            f"{self.amf_ue_ngap_id_type_len}"
            f"{self.amf_ue_ngap_id}"
            f"{self.ran_ue_ngap_id_field}"
            f"{self.ran_ue_ngap_id_type_len}"
            f"{self.ran_ue_ngap_id}"
            f"{self.nas_pdu_field}"
            f"{self.nas_pdu_type}"
            f"{self.nas_pdu_length}"
        ).upper()

    def __repr__(self):
        return (
            f"UplinkNASTransport(\n"
            f"  PDU Type: {self.pdu_type} (固定)\n"
            f"  Procedure Code: {self.procedure_code} (固定)\n"
            f"  Ngap_message_len Code: {self.ngap_message_len} \n"
            f"  Extension: {self.extension} (固定)\n"
            f"  Squence_Length: {self.squence_length} (固定)\n"
            f"  AMF-UE-NGAP-ID Field: {self.amf_ue_ngap_id_field} (固定)\n"
            f"  AMF-UE-NGAP-ID Type: {self.amf_ue_ngap_id_type_len}\n"
            f"  AMF-UE-NGAP-ID: {self.amf_ue_ngap_id}\n"
            f"  RAN-UE-NGAP-ID Field: {self.ran_ue_ngap_id_field} (固定)\n"
            f"  RAN-UE-NGAP-ID Type: {self.ran_ue_ngap_id_type_len}\n"
            f"  RAN-UE-NGAP-ID: {self.ran_ue_ngap_id}\n"
            f"  NAS-PDU Field: {self.nas_pdu_field} (固定)\n"
            f"  NAS-PDU Type: {self.nas_pdu_type}\n"
            f"  NAS-PDU Length: {self.nas_pdu_length} bytes\n"
            f")"
        )

def test():
    # 示例数据
    uplink_nas_transport_hex = "002e4067000004000a000200020055000200010026003d3c"

    # 解析 Uplink NAS Transport
    uplink_nas_transport = NGAPUplinkTransportNASMessage.parse(uplink_nas_transport_hex)

    # 打印解析结果
    print(uplink_nas_transport)

    original_hex = uplink_nas_transport.to_hex()
    print(f"Reconstructed HEX: {original_hex}")

if __name__ == "__main__":
    test()



