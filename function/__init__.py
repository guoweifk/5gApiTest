#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-18 20:16 
@file: __init__.py
@project: 5gAPItest
@describe: Powered By GW
"""
from .authReceive_Result import authReceiveAndResult
import os
import sys

# 获取当前 function 目录的绝对路径
function_path = os.path.dirname(os.path.abspath(__file__))

# 确保 function 目录在 sys.path 里
if function_path not in sys.path:
    sys.path.append(function_path)

# 自动导入 function 目录下的所有 Python 文件（去掉 __init__.py）
for module in os.listdir(function_path):
    if module.endswith(".py") and module != "__init__.py":
        module_name = module[:-3]  # 去掉 ".py"
        __import__(f"function.{module_name}")

__all__ = ["authReceiveAndResult"]