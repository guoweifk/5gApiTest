#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-24 22:21 
@file: UEMessages.py
@project: 5gAPItest
@describe: Powered By GW
"""
from UEUtils import *
import socket
from pycrate_mobile.TS24008_IE import encode_bcd
from pycrate_mobile.TS24501_IE import FGSIDTYPE_IMEISV
from pycrate_mobile.NAS import FGMMRegistrationRequest, FGMMMODeregistrationRequest, FGMMRegistrationComplete, \
    FGMMAuthenticationResponse, FGMMSecProtNASMessage, FGMMSecurityModeComplete, FGMMULNASTransport, \
    FGMMConfigurationUpdateCommand, FGMMConfigurationUpdateComplete
from pycrate_mobile.TS24501_FGSM import FGSMPDUSessionEstabRequest
from pycrate_mobile.NAS5G import parse_NAS5G
from CryptoMobile.Milenage import Milenage, make_OPc
from CryptoMobile.conv import conv_501_A2, conv_501_A4, conv_501_A6, conv_501_A7, conv_501_A8
from scapy.all import *
import binascii
import time


def registration_request(ue, IEs, Msg=None):
    """
    构建5G移动性管理(5GMM)注册请求。

    更新IEs字典，添加5GMM注册请求所需的信息，包括头信息、安全能力等，
    并将这些信息封装到消息中，更新用户设备(UE)的状态和程序计数器。

    参数:
    - ue: 用户设备对象，包含UE的特定信息，如MCC、MNC和MSIN。
    - IEs: 包含注册请求的IE（Information Elements）的字典。
    - Msg: （可选）用于构建的现有消息对象，通常为None。

    返回:
    - Msg: 构建的5GMM注册请求消息对象。
    - '5GMMRegistrationRequest': 表示消息类型的字符串。
    """
    # 设置5GMM头信息，指定协议类型和安全相关参数
    IEs['5GMMHeader'] = {'EPD': 126, 'spare': 0, 'SecHdr': 0, 'Type': 65}
    # 设置NAS密钥序列号，用于加密和完整性保护
    IEs['NAS_KSI'] = {'TSC': 0, 'Value': 7}
    # 设置5GS注册类型，表示初次注册
    IEs['5GSRegType'] = {'FOR': 1, 'Value': 1}
    # 构建5GS用户身份，包括PLMN、MSIN等信息
    IEs['5GSID'] = {'spare': 0, 'Fmt': 0, 'spare': 0, 'Type': 1, 'Value': {'PLMN': ue.mcc + ue.mnc,
                                                                           'RoutingInd': b'\x00\x00', 'spare': 0,
                                                                           'ProtSchemeID': 0, 'HNPKID': 0,
                                                                           'Output': encode_bcd(ue.msin)}}
    # 设置UE安全能力，包括支持的加密和完整性算法
    IEs['UESecCap'] = {'5G-EA0': 1, '5G-EA1_128': 1, '5G-EA2_128': 1, '5G-EA3_128': 1, '5G-EA4': 0, '5G-EA5': 0,
                       '5G-EA6': 0, '5G-EA7': 0,
                       '5G-IA0': 1, '5G-IA1_128': 1, '5G-IA2_128': 1, '5G-IA3_128': 1, '5G-IA4': 0, '5G-IA5': 0,
                       '5G-IA6': 0, '5G-IA7': 0,
                       'EEA0': 1, 'EEA1_128': 1, 'EEA2_128': 1, 'EEA3_128': 1, 'EEA4': 0, 'EEA5': 0, 'EEA6': 0,
                       'EEA7': 0,
                       'EIA0': 1, 'EIA1_128': 1, 'EIA2_128': 1, 'EIA3_128': 1, 'EIA4': 0, 'EIA5': 0, 'EIA6': 0,
                       'EIA7': 0}
    # 创建FGMM注册请求消息对象
    Msg = FGMMRegistrationRequest(val=IEs)
    # 将消息转换为字节，以便传输
    ue.MsgInBytes = Msg.to_bytes()
    # 更新UE状态为已注册（初始化阶段）
    ue.set_state(FGMMState.REGISTERED_INITIATED)
    # 设置当前程序计数器，表示正在进行的程序步骤
    ue.set_procedure(65)
    # 记录注册请求开始时间
    ue.start_time = time.time()
    # 返回构建的消息对象和消息类型
    return Msg, '5GMMRegistrationRequest'



def registration_complete(ue, IEs, Msg=None):
    IEs['5GMMHeader'] = {'EPD': 126, 'spare': 0, 'SecHdr': 0, 'Type': 67}
    # IEs['SORTransContainer'] = { 'ListInd': }
    Msg, = FGMMRegistrationComplete(val=IEs)
    ue.MsgInBytes = Msg.to_bytes()
    SecMsg = security_prot_encrypt_ciphered(ue, Msg)
    ue.set_state(FGMMState.REGISTERED)
    return SecMsg, '5GMMRegistrationComplete'
    # return Msg, '5GMMRegistrationComplete'


# TODO: handle recording of operation
def configuration_update_complete(ue, IEs, Msg=None):
    # When UE is in 5GMM-DEREGISTERED-INITIATED state ignore request (https://itecspec.com/spec/3gpp-38-523-1-9-1-6-de-registration/)
    if ue.state == FGMMState.DEREGISTERED_INITIATED:
        return None, None
    # TODO: implement action before response
    IEs['5GMMHeader'] = {'EPD': 126, 'spare': 0, 'SecHdr': 0, 'Type': 85}
    Msg = FGMMConfigurationUpdateComplete(val=IEs)
    ue.MsgInBytes = Msg.to_bytes()
    SecMsg = security_prot_encrypt_ciphered(ue, Msg)
    return SecMsg, None


def mo_deregistration_request(ue, IEs, Msg=None):
    IEs['5GMMHeader'] = {'EPD': 126, 'spare': 0, 'SecHdr': 0, 'Type': 69}
    IEs['NAS_KSI'] = {'TSC': 0, 'Value': 7}
    IEs['DeregistrationType'] = {'SwitchOff': 0, 'ReregistrationRequired': 0, 'AccessType': 1}
    IEs['5GSID'] = {'spare': 0, 'Fmt': 0, 'spare': 0, 'Type': 1, 'Value': {'PLMN': ue.mcc + ue.mnc,
                                                                           'RoutingInd': b'\x00\x00', 'spare': 0,
                                                                           'ProtSchemeID': 0, 'HNPKID': 0,
                                                                           'Output': encode_bcd(ue.msin)}}
    Msg = FGMMMODeregistrationRequest(val=IEs)
    ue.MsgInBytes = Msg.to_bytes()
    ue.set_state(FGMMState.DEREGISTERED_INITIATED)
    SecMsg = security_prot_encrypt_ciphered(ue, Msg)
    return SecMsg, '5GMMMODeregistrationRequest'


def deregistration_complete(ue, IEs, Msg=None):
    ue.set_state(FGMMState.DEREGISTERED)
    return None, '5GMMANConnectionReleaseComplete'  # For internal use only, it's not a real message type


def authentication_response(ue, IEs, Msg):
    # Msg, err = parse_NAS_MO(data)
    # if err:
    #     return
    OP = unhexlify(ue.op)
    key = unhexlify(ue.key)

    sqn_xor_ak, amf, mac = Msg['AUTN']['AUTN'].get_val()
    _, rand = Msg['RAND'].get_val()
    abba = Msg['ABBA']['V'].get_val()

    Mil = Milenage(OP)
    if ue.op_type == 'OPC':
        Mil.set_opc(OP)
    AK = Mil.f5star(key, rand)

    SQN = byte_xor(AK, sqn_xor_ak)

    Mil.f1(unhexlify(ue.key), rand, SQN=SQN, AMF=amf)
    RES, CK, IK, _ = Mil.f2345(key, rand)
    Res = conv_501_A4(CK, IK, ue.sn_name, rand, RES)

    IEs['5GMMHeader'] = {'EPD': 126, 'spare': 0, 'SecHdr': 0, 'Type': 87}
    IEs['RES'] = Res
    Msg = FGMMAuthenticationResponse(val=IEs)
    ue.MsgInBytes = Msg.to_bytes()
    # Note: See CryptoMobile.conv for documentation of this function and arguments
    # Get K_AUSF
    ue.k_ausf = conv_501_A2(CK, IK, ue.sn_name, sqn_xor_ak)
    # Get K_SEAF
    ue.k_seaf = conv_501_A6(ue.k_ausf, ue.sn_name)
    # Get K_AMF
    ue.k_amf = conv_501_A7(ue.k_seaf, ue.supi.encode('ascii'), abba)

    ue.set_state(FGMMState.AUTHENTICATED_INITIATED)
    return Msg, '5GMMAuthenticationResponse'


def security_mode_complete(ue, IEs, Msg):
    NASSecAlgo = Msg['NASSecAlgo']['NASSecAlgo'].get_val_d()
    ue.CiphAlgo = NASSecAlgo['CiphAlgo']
    ue.IntegAlgo = NASSecAlgo['IntegAlgo']
    # Get K_NAS_ENC
    ue.k_nas_enc = conv_501_A8(ue.k_amf, alg_type=1, alg_id=NASSecAlgo['CiphAlgo'])
    # Get least significate 16 bytes from K_NAS_ENC 32 bytes
    ue.k_nas_enc = ue.k_nas_enc[16:]
    # Get K_NAS_INT
    k_nas_int = conv_501_A8(ue.k_amf, alg_type=2, alg_id=NASSecAlgo['IntegAlgo'])
    ue.set_k_nas_int(k_nas_int)
    ue.k_nas_int = ue.k_nas_int[16:]
    RegIEs = {}
    RegIEs['5GMMHeader'] = {'EPD': 126, 'spare': 0, 'SecHdr': 0, 'Type': 65}
    RegIEs['NAS_KSI'] = {'TSC': 0, 'Value': 7}
    RegIEs['5GSRegType'] = {'FOR': 1, 'Value': 1}
    RegIEs['5GSID'] = {'spare': 0, 'Fmt': 0, 'spare': 0, 'Type': 1, 'Value': {'PLMN': ue.mcc + ue.mnc,
                                                                              'RoutingInd': b'\x00\x00', 'spare': 0,
                                                                              'ProtSchemeID': 0, 'HNPKID': 0,
                                                                              'Output': encode_bcd(ue.msin)}}
    RegIEs['UESecCap'] = {'5G-EA0': 1, '5G-EA1_128': 1, '5G-EA2_128': 1, '5G-EA3_128': 1, '5G-EA4': 0, '5G-EA5': 0,
                          '5G-EA6': 0, '5G-EA7': 0, '5G-IA0': 1, '5G-IA1_128': 1, '5G-IA2_128': 1, '5G-IA3_128': 1,
                          '5G-IA4': 0, '5G-IA5': 0,
                          '5G-IA6': 0, '5G-IA7': 0, 'EEA0': 1, 'EEA1_128': 1, 'EEA2_128': 1, 'EEA3_128': 1, 'EEA4': 0,
                          'EEA5': 0, 'EEA6': 0, 'EEA7': 0, 'EIA0': 1, 'EIA1_128': 1, 'EIA2_128': 1, 'EIA3_128': 1,
                          'EIA4': 0, 'EIA5': 0, 'EIA6': 0, 'EIA7': 0}
    RegIEs['5GSUpdateType'] = {
        'EPS-PNB-CIoT': 0, '5GS-PNB-CIoT': 0, 'NG-RAN-RCU': 0, 'SMSRequested': 0}
    RegIEs['5GMMCap'] = {'SGC': 0, '5G-HC-CP-CIoT': 0, 'N3Data': 0,
                         '5G-CP-CIoT': 0, 'RestrictEC': 0, 'LPP': 0, 'HOAttach': 0, 'S1Mode': 0}
    RegIEs['NSSAI'] = [{'SNSSAI': s} for s in ue.nssai]

    RegMsg = FGMMRegistrationRequest(val=RegIEs)
    IEs['5GMMHeader'] = {'EPD': 126, 'spare': 0, 'SecHdr': 0}
    IEs['IMEISV'] = {'Type': FGSIDTYPE_IMEISV, 'Digit1': int(ue.imeiSv[0]), 'Digits': ue.imeiSv[1:]}
    IEs['NASContainer'] = {}

    Msg = FGMMSecurityModeComplete(val=IEs)
    Msg['NASContainer']['V'].set_val(RegMsg.to_bytes())
    ue.MsgInBytes = Msg.to_bytes()
    # Encrypt NAS message
    SecMsg = security_prot_encrypt_ciphered(ue, Msg)
    ue.set_state(FGMMState.SECURITY_MODE_INITIATED)
    return SecMsg, '5GMMSecurityModeComplete'


def pdu_session_establishment_request(ue, IEs, Msg):
    """ 3GPP TS 24.501 version 15.7.0 6.4.1.2

    """
    IEs['5GSMHeader'] = {'EPD': 46, 'PDUSessID': 1, 'PTI': 1, 'Type': 193}
    IEs['PDUSessType'] = {'Value': 1}
    IEs['SSCMode'] = {'Value': 1}
    Msg = FGSMPDUSessionEstabRequest(val=IEs)
    ue.MsgInBytes = Msg.to_bytes()
    ULIEs = {}
    ULIEs['FGMMHeader'] = {'EPD': 46, 'spare': 0, 'SecHdr': 0, 'Type': 103}
    ULIEs['PayloadContainerType'] = {'V': 1}
    ULIEs['PDUSessID'] = 1
    ULIEs['RequestType'] = {'Value': 1}
    ULIEs['RequestType'] = {'Value': 1}
    ULIEs['SNSSAI'] = ue.nssai[0]
    ULMsg = FGMMULNASTransport(val=ULIEs)
    ULMsg['PayloadContainer']['V'].set_val(Msg.to_bytes())
    # Encrypt NAS message
    SecMsg = security_prot_encrypt_ciphered(ue, ULMsg)

    ue.set_state(FGMMState.PDU_SESSION_REQUESTED)
    return SecMsg, '5GSMPDUSessionEstabRequest'


def pdu_session_establishment_complete(ue, IEs, Msg=None):
    address = Msg['PDUAddress']['PDUAddress'].get_val_d()
    ue.IpAddress = address  # Format is {'spare': 0, 'Type': 1, 'Addr': b'\x0c\x01\x01\x07'} with type of address
    ip_addr = socket.inet_ntoa(address['Addr'])
    logger.debug(f"UE {ue.supi} assigned address {ip_addr}")
    ue.set_state(FGMMState.PDU_SESSION_ESTABLISHED)
    return None, '5GSMPDUSessionEstabComplete'  # For internal use only, it's not a real message type


def connection_release_complete(ue, IEs, Msg=None):
    ue.set_state(FGMMState.CONNECTION_RELEASED)
    ue.set_procedure(74)
    ue.end_time = time.time()
    return None, '5GMMANConnectionReleaseComplete'  # For internal use only, it's not a real message type


def pdu_session_generate_traffic(ue, IEs, Msg=None):
    ue.set_state(FGMMState.PDU_SESSION_TRANSMITTING)
    return ue.IpAddress['Addr'], '5GSMPDUSessionTransmission'