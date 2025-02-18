#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-16 22:03 
@file: helpers.py
@project: 5gAPItest
@describe: Powered By GW
"""
from Crypto.Cipher import AES
from utils import *
import hmac
import hashlib


def xor(a: bytes, b: bytes) -> bytes:
    """Byte-wise XOR of two byte sequences."""
    return bytes(x ^ y for x, y in zip(a, b))


def rot(val: bytes, r: int) -> bytes:
    """Bitwise left rotation of a 16-byte sequence by r bits."""
    int_val = int.from_bytes(val, 'big')
    rotated = ((int_val << r) | (int_val >> (128 - r))) & ((1 << 128) - 1)
    return rotated.to_bytes(16, 'big')


def Ek(K: bytes, val: bytes) -> bytes:
    """AES encryption of val using key K."""
    cipher = AES.new(K, AES.MODE_ECB)
    return cipher.encrypt(val)


def f1(K: bytes, RAND: bytes, SQN: bytes, AMF: bytes, OPc: bytes) -> tuple:
    """Compute MAC-A and MAC-S using f1 function."""
    r1 = 64
    c1 = bytearray(16)

    TEMP = Ek(K, xor(RAND, OPc))
    IN1 = SQN + AMF + SQN + AMF
    OUT1 = xor(OPc, IN1)
    OUT1 = rot(OUT1, r1)
    OUT1 = xor(Ek(K, xor(OUT1, TEMP)), OPc)

    return OUT1[:8], OUT1[8:]  # MAC-A (first 64 bits) and MAC-S (remaining 64 bits)


def f2(K: bytes, RAND: bytes, OPc: bytes) -> tuple:
    """Compute the response (RES) and anonymity key (AK) using f2 function."""
    r2 = 0
    c2 = bytearray(16)
    c2[15] = 1

    TEMP = Ek(K, xor(RAND, OPc))
    OUT2 = xor(Ek(K, xor(rot(xor(TEMP, OPc), r2), c2)), OPc)
    return OUT2[8:], OUT2[:6]  # RES (last 64 bits) and AK (first 48 bits)


def f3(K: bytes, RAND: bytes, OPc: bytes) -> bytes:
    """Compute the confidentiality key (CK) using f3 function."""
    r3 = 32
    c3 = bytearray(16)
    c3[15] = 2

    TEMP = Ek(K, xor(RAND, OPc))
    OUT3 = xor(Ek(K, xor(rot(xor(TEMP, OPc), r3), c3)), OPc)
    return OUT3


def f4(K: bytes, RAND: bytes, OPc: bytes) -> bytes:
    """Compute the integrity key (IK) using f4 function."""
    r4 = 64
    c4 = bytearray(16)
    c4[15] = 4

    TEMP = Ek(K, xor(RAND, OPc))
    OUT4 = xor(Ek(K, xor(rot(xor(TEMP, OPc), r4), c4)), OPc)
    return OUT4


def f5_star(K: bytes, RAND: bytes, OPc: bytes) -> bytes:
    """Compute the anonymity key (AK*) using f5* function."""
    r5 = 96
    c5 = bytearray(16)
    c5[15] = 8

    TEMP = Ek(K, xor(RAND, OPc))
    OUT5 = xor(Ek(K, xor(rot(xor(TEMP, OPc), r5), c5)), OPc)
    return OUT5[:6]  # AK* is the first 48 bits of OUT5

def hmac_sha256(data: bytes, key: bytes) -> bytes:
    """使用 HMAC-SHA256 计算消息认证码"""
    return hmac.new(key, data, hashlib.sha256).digest()


def hmac_sha256_octet_string(key: OctetString, input_data: OctetString) -> OctetString:
    """封装的 HMAC-SHA256 计算，返回 OctetString"""
    return OctetString(hmac_sha256(input_data.value, key.value))

def main():
    """Main function to compute and display MILENAGE results."""
    # Input values
    K = bytes.fromhex("465B5CE8B199B49FAA5F0A2EE238A6BC")
    OPc = bytes.fromhex("E8ED289DEBA952E4283B54E88E6183CA")
    RAND = bytes.fromhex("5439cc5a3f65c2f14ab5628f6c4a0b28")

    # Compute CK, IK, RES, AK, and AK*
    RES, AK = f2(K, RAND, OPc)
    CK = f3(K, RAND, OPc)
    IK = f4(K, RAND, OPc)
    AK_star = f5_star(K, RAND, OPc)

    # Print results
    print("CK:", CK.hex().upper())
    print("IK:", IK.hex().upper())
    print("RES:", RES.hex().upper())
    print("AK:", AK.hex().upper())
    print("AK*:", AK_star.hex().upper())

if __name__ == "__main__":
    main()


    # CK: 81233D13ADC283AFD9C0DC5106D7CE6E
    # IK: B9AC53FC1B915D380A7ACB9686439275
    # AK*: B557B799074F
