#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-04-25 15:06 
@file: pcf_create.py
@project: 5gAPItest
@describe: Powered By GW
"""
import httpx

# PCF 地址
url = "http://127.0.0.200:7777/npcf-smpolicycontrol/v1/sm-policies"

# HTTP Headers
headers = {
    "accept": "application/json,application/problem+json",
    "content-type": "application/json"
}

# JSON 消息体
payload = {
    "supi": "imsi-001010000000000",
    "pduSessionId": 1,
    "pduSessionType": "IPV4",
    "chargingcharacteristics": "00000800",
    "dnn": "internet",
    "notificationUri": "http://127.0.0.4:7777/nsmf-callback/v1/sm-policy-notify/5",
    "ratType": "NR",
    "servingNetwork": {"mcc": "001", "mnc": "01"},
    "userLocationInfo": {
        "nrLocation": {
            "tai": {"plmnId": {"mcc": "001", "mnc": "01"}, "tac": "000001"},
            "ncgi": {"plmnId": {"mcc": "001", "mnc": "01"}, "nrCellId": "000000010"},
            "ueLocationTimestamp": "2025-04-25T05:47:22.833314Z"
        }
    },
    "ueTimeZone": "+08:00",
    "ipv4Address": "10.45.0.6",
    "subsSessAmbr": {"uplink": "1000000 Kbps", "downlink": "1000000 Kbps"},
    "subsDefQos": {
        "5qi": 9,
        "arp": {
            "priorityLevel": 8,
            "preemptCap": "NOT_PREEMPT",
            "preemptVuln": "NOT_PREEMPTABLE"
        },
        "priorityLevel": 8
    },
    "sliceInfo": {"sst": 1},
    "suppFeat": "4000000"
}

# 发送 HTTP/2 请求
with httpx.Client(http2=True) as client:
    response = client.post(url, headers=headers, json=payload)
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)


# with httpx.Client(http2=True) as client:
#     while True:
#         try:
#             response = client.post(url, headers=headers, json=payload)
#             print(f"Status: {response.status_code}, Response: {response.text}")
#         except Exception as e:
#             print(f"Request failed: {e}")
#         # time.sleep(1)  # 每秒发送一次（根据需要调节）