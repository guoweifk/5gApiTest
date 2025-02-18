#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-17 11:16
@file: calculateResStar.py
@project: 5gAPItest
@describe: Powered By GW
"""
from utils.helpers import f1,f2,f3,f4,hmac_sha256_octet_string
from typing import List
from utils import *

AMF = bytes.fromhex("8000")  # 2字节 AMF
SNN = "5G:mnc001.mcc001.3gppnetwork.org"
K = bytes.fromhex("465B5CE8B199B49FAA5F0A2EE238A6BC")  # 16字节密钥 K
OPc = bytes.fromhex("E8ED289DEBA952E4283B54E88E6183CA")  # 16字节 OPc

def calculate(opc: OctetString, key: OctetString, rand: OctetString, sqn_xor_ak: OctetString, amf: OctetString) -> Milenage:
    r = Milenage(op=opc, key=key, opType="opc",rand = rand)
    # opc = calculate_opc(opc,key)

    # 调用 data() 方法，获取 bytes 数据
    res, ak = f2(key, rand, opc)
    r.res, r.ak = OctetString(res), OctetString(ak)
    # 计算SQN
    r.sqn = OctetString.xor(sqn_xor_ak, r.ak)
    print(f"sqn: {r.sqn}")
    print(f"sqn_xor_ak: {sqn_xor_ak.hex()}")

    mac_a, mac_s = f1(key,rand,r.sqn.value, amf,opc)
    r.mac_a, r.mac_s = OctetString(mac_a), OctetString(mac_s)
    r.ck = OctetString(f3(key, rand, opc))
    r.ik = OctetString(f4(key, rand, opc))
    # 计算 CK || IK 和 SQN ⊕ AK
    r.ck_ik = OctetString.concat(r.ck, r.ik)

    # 输出所有 R 的内容

    print(f"ck_ik: {r.ck_ik}")
    return r

def encode_kdf_string(string: str) -> OctetString:
    # 归一化字符串 (NFKC)
    # normalized_string = unicodedata.normalize("NFKC", string)

    # 进行 UTF-8 编码
    encoded_bytes = string.encode("utf-8")

    # 返回 OctetString 对象
    return OctetString(encoded_bytes)

def calculate_res_star(key: OctetString, snn: str, rand: OctetString, res: OctetString) -> OctetString:
    """计算 5G RES* (XRES*)"""
    print(f"params: {encode_kdf_string(snn)}")
    params = [
        encode_kdf_string(snn),  # 归一化 SNN
        OctetString(rand.value[:]),  # 复制 RAND
        OctetString(res.value[:])  # 复制 RES
    ]
    print(f"params: {params}")

    output = calculate_kdf_key(key, 0x6B, params)  # 计算 KDF
    print(f"kdf_key: {output}")
    return OctetString(output.value[-16:])  # 取最后 16 字节作为 RES*

def calculate_kdf_key(key: OctetString, fc: int, parameters: List[OctetString]) -> OctetString:

    """计算 KDF (Key Derivation Function)"""
    inp = OctetString()
    inp.append_octet(fc)  # 添加 FC (Function Code)

    for param in parameters:
        inp.append(param)  # 追加参数值
        inp.append_octet2(param.length())  # 追加参数长度 (2 字节)

    return hmac_sha256_octet_string(key, inp)  # 计算 HMAC-SHA256

def calculateResStar(rand: bytes, sqn_xor_ak: bytes):
    milenage = calculate(OPc, K, rand.hex(), OctetString(sqn_xor_ak.hex()), AMF)
    m_resStar = calculate_res_star(milenage.ck_ik, SNN, OctetString(milenage.rand), milenage.res)
    return m_resStar

def test():
    # ==== 计算 Milenage 并计算 RES* ====
    RAND = bytes.fromhex("5439cc5a3f65c2f14ab5628f6c4a0b28")  # 16字节随机数
    sqn_xor_ak = bytes.fromhex("21ea888a0065")  # 6字节 SQN
    print(RAND)
    milenage = calculate(OPc, K, RAND, sqn_xor_ak, AMF)
    m_resStar = calculate_res_star(milenage.ck_ik, SNN, OctetString(milenage.rand), milenage.res)

    # ==== 输出结果 ====
    print("m_resStar:", m_resStar.value.hex())


if __name__ == "__main__":
    test()
    # 测试用例
    # SNN = "5G:mnc001.mcc001.3gppnetwork.org"
    # K = bytes.fromhex("465B5CE8B199B49FAA5F0A2EE238A6BC")  # 16字节密钥 K
    # OPc = bytes.fromhex("E8ED289DEBA952E4283B54E88E6183CA")  # 16字节 OPc
    # RAND = bytes.fromhex("5439cc5a3f65c2f14ab5628f6c4a0b28")  # 16字节随机数
    # SQN = bytes.fromhex("0000000002C1")  # 6字节 SQN
    # AMF = bytes.fromhex("8000")  # 2字节 AMF
    # ck_ik = OctetString(bytes.fromhex("81233D13ADC283AFD9C0DC5106D7CE6EB9AC53FC1B915D380A7ACB9686439275"))
    # MAC-A: OctetString(a6bea3f1d4ae4da4)
    # MAC-S: OctetString(0e1c31faeeb0196d)
    # sqn_xor_ak-R: OctetString(21ea888a0065)
    # params: OctetString(35473a6d6e633030312e6d63633030312e336770706e6574776f726b2e6f7267)
    # params: [OctetString(35473a6d6e633030312e6d63633030312e336770706e6574776f726b2e6f7267), OctetString(5439cc5a3f65c2f14ab5628f6c4a0b28), OctetString(3b438ec21ff371d9)]
    # kdf_key: OctetString(8fcb30174135238ddcdb4015058b4c91c99a673b7ee90bdab0cc5ce3a4fe4b40)
    # m_resStar: c99a673b7ee90bdab0cc5ce3a4fe4b40