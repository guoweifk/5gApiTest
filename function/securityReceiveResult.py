#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-19 11:33 
@file: securityReceiveResult.py
@project: 5gAPItest
@describe: Powered By GW
"""
# 安全的信息调用这个pycrate_mobile 中
from message import *
import time
from pycrate_mobile import *
from pycrate_mobile.NAS5G import parse_NAS5G
from CryptoMobile.conv import *
from message.UEUtils import *
from CryptoMobile.conv import conv_501_A2, conv_501_A4, conv_501_A6, conv_501_A7, conv_501_A8


def security_mode_complete(kseaf):
    # print(kseaf)
    # NASSecAlgo = Msg['NASSecAlgo']['NASSecAlgo'].get_val_d()
    ciphAlgo = 0
    ntegAlgo = 2
    # Get K_NAS_ENC
    SNN = b"5G:mnc001.mcc001.3gppnetwork.org"
    SPUI= b"001010000000000"
    ABBA = b'\x00\x00'
    k_amf = conv_501_A7(kseaf, SPUI, ABBA)
    k_nas_enc = conv_501_A8(k_amf, alg_type=1, alg_id=ciphAlgo)
    # Get least significate 16 bytes from K_NAS_ENC 32 bytes
    k_nas_enc = k_nas_enc[16:]
    print("k_nas_enc:" ,k_nas_enc)
    # Get K_NAS_INT
    k_nas_int = conv_501_A8(k_amf, alg_type=2, alg_id=ntegAlgo)
    print("k_nas_int:", k_nas_int)
    k_nas_int = k_nas_int[16:]
    RegIEs = {}
    RegIEs['5GMMHeader'] = {'EPD': 126, 'spare': 0, 'SecHdr': 0, 'Type': 65}
    RegIEs['NAS_KSI'] = {'TSC': 0, 'Value': 7}
    RegIEs['5GSRegType'] = {'FOR': 1, 'Value': 1}
    mcc = "001"
    mnc = "01"
    msin = "0000000000"
    imeisv = "4370816125816151"
    RegIEs['5GSID'] = {'spare': 0, 'Fmt': 0, 'spare': 0, 'Type': 1, 'Value': {'PLMN': mcc + mnc,
                                                                              'RoutingInd': b'\x00\x00', 'spare': 0,
                                                                              'ProtSchemeID': 0, 'HNPKID': 0,
                                                                              'Output': encode_bcd(msin)}}
    RegIEs['UESecCap'] = {'5G-EA0': 1, '5G-EA1_128': 1, '5G-EA2_128': 1, '5G-EA3_128': 1, '5G-EA4': 0, '5G-EA5': 0,
                          '5G-EA6': 0, '5G-EA7': 0, '5G-IA0': 1, '5G-IA1_128': 1, '5G-IA2_128': 1, '5G-IA3_128': 1,
                          '5G-IA4': 0, '5G-IA5': 0,
                          '5G-IA6': 0, '5G-IA7': 0, 'EEA0': 1, 'EEA1_128': 1, 'EEA2_128': 1, 'EEA3_128': 1, 'EEA4': 0,
                          'EEA5': 0, 'EEA6': 0, 'EEA7': 0, 'EIA0': 1, 'EIA1_128': 1, 'EIA2_128': 1, 'EIA3_128': 1,
                          'EIA4': 0, 'EIA5': 0, 'EIA6': 0, 'EIA7': 0}
    RegIEs['5GSUpdateType'] = {
        'EPS-PNB-CIoT': 0, '5GS-PNB-CIoT': 0, 'NG-RAN-RCU': 0, 'SMSRequested': 0}
    # RegIEs['5GMMCap'] = {'SGC': 0, '5G-HC-CP-CIoT': 0, 'N3Data': 0,
    #                      '5G-CP-CIoT': 0, 'RestrictEC': 0, 'LPP': 0, 'HOAttach': 0, 'S1Mode': 0}
    RegIEs['5GMMCap'] = {'SGC': 0, '5G-HC-CP-CIoT': 0, 'N3Data': 0,
                         '5G-CP-CIoT': 0, 'RestrictEC': 0, 'LPP': 0, 'HOAttach': 0, 'S1Mode': 0}

    nssai = [{'SST': 1}]
    # msg['SNSSAI'][1] = {'SST': 1}
    RegIEs['NSSAI'] = [{'SNSSAI': s} for s in nssai]

    RegMsg = FGMMRegistrationRequest(val=RegIEs)
    # RegMsg['5GMMCap']['V'].set_val(b'\x01\x00')
    RegMsg['5GMMCap']['5GMMCap'].disable_from(8)

    IEs = {}
    IEs['5GMMHeader'] = {'EPD': 126, 'spare': 0, 'SecHdr': 0}
    IEs['IMEISV'] = {'Type': FGSIDTYPE_IMEISV, 'Digit1': int(imeisv[0]), 'Digits': imeisv[1:]}
    IEs['NASContainer'] = {}

    Msg = FGMMSecurityModeComplete(val=IEs)
    Msg['NASContainer']['V'].set_val(RegMsg.to_bytes())
    MsgInBytes = Msg.to_bytes()
    # Encrypt NAS message
    SecMsg = security_prot_encrypt_ciphered(ciphAlgo, ntegAlgo, k_nas_enc, k_nas_int, Msg)
    # ue.set_state(FGMMState.SECURITY_MODE_INITIATED)
    return SecMsg, '5GMMSecurityModeComplete'


def securityReceiveAndResult(KSEAF, security_request: bytes):
    ngap_header, nas_pdu = split_ngap_nas(security_request)
    ngap_downlink_message = NGAPDownLinkTransportNASMessage.parse(ngap_header)
    # 转换为十六进制格式（大写）
    current_timestamp = int(time.time())
    hex_timestamp = format(current_timestamp, 'X')
    ngap_uplink_message = NGAPUplinkTransportNASMessage(
        amf_ue_ngap_id=ngap_downlink_message.amf_ue_ngap_id,
        ran_ue_ngap_id=ngap_downlink_message.ran_ue_ngap_id,
        nas_pdu_type="003d",
        nas_pdu_length="3c",
        ngap_message_len="67"
    )

    # security_request_message = AuthenticationRequestMessage.parse(nas_pdu)
    # print(ngap_downlink_message)
    # print(security_request_message)
    secMesg = security_mode_complete(KSEAF)
    # print(secMesg)
    security_response_message = "7e04f15f1642007e005e7700094573806121856151f17100237e004179000d0100f1100000000000000000001001002e04f0f0f0f02f020101530100007940135000f110000000010000f110000001eb5da5ba"
    # "7e005e7700094573806121856151f17100277e004179000d0100f110000000000000000000100500000000002e04f0f0f0f02f020101530100"

    # "7e04f15f1642007e005e7700094573806121856151f17100277e004179000d0100f110000000000000000000100500000000002e04f0f0f0f02f020101530100007940135000f110000000010000f110000001eb5da5ba"
    "7e04f15f1642007e005e7700094573806121856151f17100207e004179000d0100f1100000000000000000002e04f0f0f0f02f020101530100007940135000f110000000010000f110000001eb5da5ba100100"

    # "7e04f15f1642007e005e7700094573806121856151f17100237e004179000d0100f1100000000000000000001001002e04f0f0f0f02f020101530100007940135000f110000000010000f110000001eb5da5ba"
    security_response_message = "7e04" + hexlify(secMesg[0]['MAC'].get_val()).decode(
        'utf-8') + "00" + hexlify(
        secMesg[0]['NASMessage'].get_val()).decode(
        'utf-8') + "007940135000f110000000010000f110000001eb5da5ba"
    # print(security_response_message)
    return ngap_uplink_message.to_hex() + security_response_message


def test():
    # 假设 nas_message 是一个包含 5G NAS 消息的字节对象
    nas_message = "7e0323b43810007e005d020304f0f0f0f0e1360102"  # 示例字节流

    # 调用 parse_NAS5G 函数解析消息
    parsed_message, error_code = parse_NAS5G(bytes.fromhex(nas_message))

    if error_code == 0:
        print("解析成功:")
        print(parsed_message)
    else:
        print(f"解析失败，错误码: {error_code}")


if __name__ == "__main__":
    test()
