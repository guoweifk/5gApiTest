#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-03 22:56 
@file: sbi_processer.py
@project: 5gAPItest
@describe: Powered By GW
"""

class SBIClientProcessor:
    def __init__(self, connection):
        self.connection = connection
        self.steps = []

    def add_step(self, message_class):
        self.steps.append(message_class(self.connection))

    def run(self):
        for i, step in enumerate(self.steps):
            print(f"\n[STEP {i+1}] {step.__class__.__name__}")
            try:
                step.send()
            except Exception as e:
                print(f"[ERROR] Failed at {step.__class__.__name__}: {e}")
                break
        self.connection.close()
