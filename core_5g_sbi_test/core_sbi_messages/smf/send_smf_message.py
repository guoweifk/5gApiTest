#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-04-25 14:19 
@file: send_smf_message.py
@project: 5gAPItest
@describe: Powered By GW
"""
import httpx

# SMF 地址
url = "http://127.0.0.200:7777/nsmf-pdusession/v1/sm-contexts"

# Multipart Boundary
boundary = "--boundary123"

# HTTP Headers
headers = {
    "content-type": f'multipart/related; boundary="{boundary}"',
    "accept": "application/json,application/problem+json"
}

# Multipart Body（JSON + NAS SM）
json_part = (
    f'--{boundary}\r\n'
    'Content-Type: application/json\r\n\r\n'
    '{'
    '"supi": "imsi-001010000000000",'
    '"pduSessionId": 1,'
    '"dnn": "internet",'
    '"sNssai": {"sst": 1},'
    '"guami": {"plmnId": {"mcc": "001", "mnc": "01"}, "amfId": "020040"},'
    '"servingNetwork": {"mcc": "001", "mnc": "01"},'
    '"n1SmMsg": {"contentId": "5gnas-sm"},'
    '"anType": "3GPP_ACCESS",'
    '"ratType": "NR",'
    '"ueLocation": {'
        '"nrLocation": {'
            '"tai": {"plmnId": {"mcc": "001", "mnc": "01"}, "tac": "000001"},'
            '"ncgi": {"plmnId": {"mcc": "001", "mnc": "01"}, "nrCellId": "000000010"}'
        '}'
    '}'
    '}\r\n'
)

nas_sm_msg = b'\x7e\x00\x01\x02\x03\x04'  # 示例NAS数据

nas_part = (
    f'--{boundary}\r\n'
    'Content-Id: 5gnas-sm\r\n'
    'Content-Type: application/vnd.3gpp.5gnas\r\n\r\n'
).encode() + nas_sm_msg + b'\r\n'

end_boundary = f'--{boundary}--'.encode()

# 拼接完整请求体
body = json_part.encode() + nas_part + end_boundary

# 发送 HTTP/2 请求
with httpx.Client(http2=True) as client:
    response = client.post(url, headers=headers, content=body)
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)
