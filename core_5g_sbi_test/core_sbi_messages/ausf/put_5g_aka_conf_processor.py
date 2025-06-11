#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-04 19:43 
@file: put_5g_aka_conf_processor.py
@project: 5gAPItest
@describe: Powered By GW
"""
from core_5g_sbi_test.core_sbi_messages.sbi_base_processor import SBIBaseProcessor
import json
import time
from email.utils import formatdate
import random

class Put5gAkaConfirmationProcessor(SBIBaseProcessor):
    def __init__(self, connection):
        super().__init__(connection)

    def sender(self):
        return "AMF"

    def receiver(self):
        return "AUSF"

    def build_headers(self, body: dict = None):
        return [
            (':method', 'PUT'),
            (':path', '/nausf-auth/v1/ue-authentications/1/5g-aka-confirmation'),
            (':scheme', 'http'),
            (':authority', f'{self.connection.host}:{self.connection.port}'),
            ('content-type', 'application/json'),
            ('accept', 'application/json,application/problem+json'),
            ('content-length', str(len(json.dumps(body).encode('utf-8')) if body else 0)),
            ('user-agent', 'AMF'),
            ('3gpp-sbi-sender-timestamp', time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())),
            ('3gpp-sbi-max-rsp-time', '10000')
        ]

    def build_body(self):
        return {
            "resStar": "0deaf60b6d0b6ffa764eb869492d8315"
        }

    def match(self, path: str) -> bool:
        return path.startswith("/nausf-auth/v1/ue-authentications/") and path.endswith("/5g-aka-confirmation")

    def handle(self, stream_id, conn, headers: list):
        response_body_dict = {
            "authResult": random.choice([
                "AUTHENTICATION_SUCCESS",
                "AUTHENTICATION_FAILURE",
                "AUTHENTICATION_ONGOING"

            ]),
            "supi": "imsi-001010000000000",
            "kseaf": "46a2be1ee40464e0d92d10645b312196daa632c485a64951e482ed5ca657f32b"
        }

        response_body = json.dumps(response_body_dict).encode("utf-8")

        response_headers = [
            (':status', '200'),
            ('server', 'Open5GS v2.7.5-5-g1182a99'),
            ('date', formatdate(timeval=None, localtime=False, usegmt=True)),
            ('content-type', 'application/json'),
            ('content-length', str(len(response_body)))
        ]

        return response_headers, response_body
