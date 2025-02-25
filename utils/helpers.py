#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-16 22:03 
@file: helpers.py
@project: 5gAPItest
@describe: Powered By GW
"""

def byte_xor(ba1, ba2):
    """ XOR two byte strings """
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
