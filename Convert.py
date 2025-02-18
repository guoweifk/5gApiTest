#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-13 17:03 
@file: Convert.py
@project: 5gAPItest
@describe: Powered By GW
"""
import struct
from typing import List

def bytes_to_hex(data: bytes) -> str:
    return ''.join(f"{b:02X}" for b in data)

def int_to_bytes(data: int) -> bytes:
    return shrink_bytes(data.to_bytes((data.bit_length() + 7) // 8 or 1, byteorder='big'))

def bytes_to_int(data: bytes) -> int:
    if not data:
        return 0
    expanded_data = expand_bytes_to_length(data, 4) if len(data) < 4 else data
    return struct.unpack('>I', expanded_data)[0]

def shrink_bytes(data: bytes) -> bytes:
    index = next((i for i, b in enumerate(data) if b != 0), len(data))
    return data[index:] if index < len(data) else data

def expand_bytes_to_length(data: bytes, length: int) -> bytes:
    if data is None:
        return bytes(length)
    if length < len(data):
        return data
    return bytes(length - len(data)) + data

def concatenate_bytes(*data: List[bytes]) -> bytes:
    return b''.join(data)

def split_bytes(data: bytes, *lengths: List[int]) -> List[bytes]:
    index = 0
    result = []
    for length in lengths:
        if index >= len(data):
            result.append(b'')
        elif index + length > len(data):
            result.append(data[index:])
        else:
            result.append(data[index:index + length])
        index += length
    return result