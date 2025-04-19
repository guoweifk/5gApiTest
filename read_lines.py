#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-04-02 18:01 
@file: read_lines.py
@project: 5gAPItest
@describe: Powered By GW
"""
log_lines = [
    "[Thread 381] Error: invalid literal for int() with base 16: ''",
    "[Thread 381] Connection closed.",
    "[Thread 2] Connected and sending data...",
    "[Thread 7] Error: [Errno 111] Connection refused"
    # ... 这里可以添加更多类似的行
]

# 提取 [] 中间内容的 set
thread_ids = set()

for line in log_lines:
    match = re.search(r'\[(.*?)\]', line)
    if match:
        thread_ids.add(match.group(1))

print(thread_ids)
