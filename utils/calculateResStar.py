#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-17 11:16
@file: calculateResStar.py
@project: 5gAPItest
@describe: Powered By GW
"""

from CryptoMobile.Milenage import Milenage
from CryptoMobile.Milenage import make_OPc
from CryptoMobile.conv import *
from CryptoMobile.ECIES import *

AMF = bytes.fromhex("8000")  # 2字节 AMF
SNN = b"5G:mnc001.mcc001.3gppnetwork.org"
K = bytes.fromhex("465B5CE8B199B49FAA5F0A2EE238A6BC")  # 16字节密钥 K
OPc = bytes.fromhex("E8ED289DEBA952E4283B54E88E6183CA")  # 16字节 OPc

def byte_xor(ba1, ba2):
    """ XOR two byte strings """
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

# 调用库函数
def calculateRes(rand: bytes, sqn_xor_ak: bytes):
    Mil = Milenage(OPc)
    Mil.set_opc(OPc)
    RES, CK, IK, AK = Mil.f2345(K, rand)
    SQN = byte_xor(AK, sqn_xor_ak)
    mac_a = Mil.f1(K, rand, SQN=SQN, AMF=AMF)
    Res = conv_501_A4(CK, IK, SNN, rand, RES)
    KAUSF = conv_501_A2(CK, IK, SNN, sqn_xor_ak)
    # print("KAUSF: ", hexlify(KAUSF))
    KSEAF = conv_501_A6(KAUSF,SNN)
    # print("KSEAF: ", hexlify(KSEAF))

    # print("AK: ", hexlify(AK))
    # print("SQN: ", hexlify(SQN))
    # print(mac_a)
    # print(hexlify(CK))
    # print ("RES: ",hexlify(RES))
    return KSEAF,Res.hex()

def test():
    # ==== 计算 Milenage 并计算 RES* ====
    RAND = bytes.fromhex("5439cc5a3f65c2f14ab5628f6c4a0b28")  # 16字节随机数
    sqn_xor_ak = bytes.fromhex("21ea888a0065")  # 6字节 SQN
    print(RAND)
    m_resStar = calculateRes(RAND,sqn_xor_ak)
    # ==== 输出结果 ====
    print("m_resStar:", m_resStar)


if __name__ == "__main__":
    test()
    # 测试用例
    # SNN = "5G:mnc001.mcc001.3gppnetwork.org"
    # K = bytes.fromhex("465B5CE8B199B49FAA5F0A2EE238A6BC")  # 16字节密钥 K
    # OPc = bytes.fromhex("E8ED289DEBA952E4283B54E88E6183CA")  # 16字节 OPc
    # RAND = bytes.fromhex("5439cc5a3f65c2f14ab5628f6c4a0b28")  # 16字节随机数
    # SQN = bytes.fromhex("0000000002C1")  # 6字节 SQN
    # AK = OctetString(21ea888a02a4)
    # RES = OctetString(3b438ec21ff371d9)
    # AMF = bytes.fromhex("8000")  # 2字节 AMF
    # ck_ik = OctetString(bytes.fromhex("81233D13ADC283AFD9C0DC5106D7CE6EB9AC53FC1B915D380A7ACB9686439275"))
    # MAC-A: OctetString(a6bea3f1d4ae4da4)
    # MAC-S: OctetString(0e1c31faeeb0196d)
    # sqn_xor_ak-R: OctetString(21ea888a0065)
    # params: OctetString(35473a6d6e633030312e6d63633030312e336770706e6574776f726b2e6f7267)
    # params: [OctetString(35473a6d6e633030312e6d63633030312e336770706e6574776f726b2e6f7267), OctetString(5439cc5a3f65c2f14ab5628f6c4a0b28), OctetString(3b438ec21ff371d9)]
    # kdf_key: OctetString(8fcb30174135238ddcdb4015058b4c91c99a673b7ee90bdab0cc5ce3a4fe4b40)
    # m_resStar: c99a673b7ee90bdab0cc5ce3a4fe4b40