#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-18 9:55 
@file: __init__.py.py
@project: 5gAPItest
@describe: Powered By GW
"""
# utils/__init__.py

from .octet_string import OctetString
from .milenage import Milenage
import os
import sys

# 获取当前 utils 目录的绝对路径
utils_path = os.path.dirname(os.path.abspath(__file__))

# 确保 utils 目录在 sys.path 里
if utils_path not in sys.path:
    sys.path.append(utils_path)

# 自动导入 utils 目录下的所有 Python 文件（去掉 __init__.py）
for module in os.listdir(utils_path):
    if module.endswith(".py") and module != "__init__.py":
        module_name = module[:-3]  # 去掉 ".py"
        __import__(f"utils.{module_name}")



__all__ = ["OctetString","Milenage"]