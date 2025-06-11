#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-06-04 19:40 
@file: post_ue_au_data.py
@project: 5gAPItest
@describe: Powered By GW
"""
from core_5g_sbi_test.core_sbi_messages.sbi_base_processor import SBIBaseProcessor
import json
import time
from email.utils import formatdate


class PostUeAuthenticationProcessor(SBIBaseProcessor):
    def __init__(self, connection):
        super().__init__(connection)

    def sender(self):
        return "AMF"

    def receiver(self):
        return "AUSF"

    def build_headers(self, body: dict = None):
        return [
            (':method', 'POST'),
            (':path', '/nausf-auth/v1/ue-authentications'),
            (':scheme', 'http'),
            (':authority', f'{self.connection.host}:{self.connection.port}'),
            ('accept', 'application/3gppHal+json,application/problem+json'),
            ('3gpp-sbi-sender-timestamp', time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())),
            ('3gpp-sbi-max-rsp-time', '10000'),
            ('content-type', 'application/json'),
            ('content-length', str(len(json.dumps(body).encode('utf-8')) if body else 0)),
            ('user-agent', 'AMF')
        ]

    def build_body(self):
        return {
            "supiOrSuci": "suci-0-001-01-0000-0-0-0000000000",
            "servingNetworkName": "5G:mnc001.mcc001.3gppnetwork.org"
        }

    def match(self, path: str) -> bool:
        return (
                "/nausf-auth/v1/ue-authentications" in path
        )

    def handle(self, stream_id, conn, headers: list):
        response_body_dict = {
            "authType": "5G_AKA",
            "5gAuthData": {
                "rand": "16bbf88766468dea5871c244e3618b0d",
                "hxresStar": "091da53b5b2b1850f0545f08b872a653",
                "autn": "374ebb2dcb018000777ba66c58ccf3dc"
            },
            "_links": {
                "5g-aka": {
                    "href": "http://127.0.0.11:7777/nausf-auth/v1/ue-authentications/1/5g-aka-confirmation"
                }
            }
        }

        response_body = json.dumps(response_body_dict).encode("utf-8")

        response_headers = [
            (':status', '201'),
            ('server', 'Open5GS v2.7.5-5-g1182a99'),
            ('date', formatdate(timeval=None, localtime=False, usegmt=True)),
            ('content-length', str(len(response_body))),
            ('location', 'http://127.0.0.11:7777/nausf-auth/v1/ue-authentications/1'),
            ('content-type', 'application/3gppHal+json')
        ]

        return response_headers, response_body
