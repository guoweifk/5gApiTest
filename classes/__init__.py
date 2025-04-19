#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-24 20:54 
@file: __init__.py.py
@project: 5gAPItest
@describe: Powered By GW
"""
import os
import sys
from .SCTP import SCTPClient
from .InterfaceConfig import InterfaceConfig
from .GTPU import GTPU,GTPUConfig
from .NGAPSim import GNB
from .UESim import UESim
from .UE import UE

# 获取当前 class_path 目录的绝对路径
class_path = os.path.dirname(os.path.abspath(__file__))

# 确保 class_path 目录在 sys.path 里
if class_path not in sys.path:
    sys.path.append(class_path)

# 自动导入 class_path 目录下的所有 Python 文件（去掉 __init__.py）
for module in os.listdir(class_path):
    if module.endswith(".py") and module != "__init__.py":
        module_name = module[:-3]  # 去掉 ".py"
        __import__(f"classes.{module_name}")

__all__ = ["InterfaceConfig", "SCTPClient", "UE", "GNB", "UESim", "GTPU", "GTPUConfig"]
