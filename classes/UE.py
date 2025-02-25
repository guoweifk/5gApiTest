#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: GW
@time: 2025-02-24 22:20 
@file: UE.py
@project: 5gAPItest
@describe: Powered By GW
"""
import sys
import time
import logging
import threading
import time
import traceback
import signal
from functools import partial
from itertools import product
# from tabulate import tabulate
from pycrate_mobile.NAS5G import parse_NAS5G, parse_PayCont
from message.UEMessages import *
from message.ComplianceTestUEMessages import *
from message.UEUtils import *
import psutil
import multiprocessing

request_mapper = {
    '5GMMRegistrationRequest': registration_request,
    '5GSMPDUSessionEstabRequest': pdu_session_establishment_request,
    '5GMMMODeregistrationRequest': mo_deregistration_request,
    '5GSMPDUSessionTransmission': pdu_session_generate_traffic
}

response_mapper = {
    '5GMMAuthenticationRequest': authentication_response,
    '5GMMRegistrationAccept': registration_complete,
    '5GMMConfigurationUpdateCommand': configuration_update_complete,
    '5GSMPDUSessionEstabAccept': pdu_session_establishment_complete,
    '5GMMSecurityModeCommand': security_mode_complete,
    '5GMMMODeregistrationAccept': deregistration_complete,
    '5GMMANConnectionReleaseComplete': connection_release_complete
}

compliance_test_mapper = {
    '5GMMRegistrationRequest': [registration_request],
    '5GMMAuthenticationRequest': [authentication_response, authentication_response_invalid_rand],
    '5GMMRegistrationAccept': [registration_complete],
    '5GMMSecurityModeCommand': [security_mode_complete, security_mode_complete_missing_nas_container],
    '5GSMPDUSessionEstabRequest': [pdu_session_establishment_request],
    '5GMMMODeregistrationRequest': [mo_deregistration_request],
    '5GMMMODeregistrationAccept': [deregistration_complete]
}


# TODO: complete and incoperate the validator
def validator(PrevMsgBytesSent, MsgRecvd):
    """
        Checks the last message sent against the message received to see if it is the expected response.
        It logs the mismatch if any is detected
    """

    PrevMsgSent, err = parse_NAS5G(PrevMsgBytesSent)
    if err:
        logger.error(f"Failed to parse the UE's previous message {PrevMsgSent}")
        return
    recv_msg_name = None
    MsgRecvdDict = {}
    if MsgRecvd == b'F':
        recv_msg_name = '5GMMANConnectionReleaseComplete'
    elif MsgRecvd == b'0':
        recv_msg_name = 'program teminated before receiving the expected response, the 5GC might not have responded'
        error_message = f"Expected response but {recv_msg_name}"
        return FGMMState.NO_RESPONSE, error_message
    else:
        recv_msg_name = MsgRecvd._name
        MsgRecvdDict = MsgRecvd.get_val_d()

    PrevMsgSentDict = PrevMsgSent.get_val_d()

    # Check if the received message doesn't have a response mapped
    if not recv_msg_name in response_mapper:
        # This is not an error, log for info purposes
        logger.info(f"Received {recv_msg_name} a message without a response mapped to it")

    if PrevMsgSent._name == '5GMMRegistrationRequest':
        """ General Registration procedure 3GPP TS 23.502 4.2.2.2.2

        Depending on the parameter provided and whether it's moving from an old AMF, the next
        message from the CN is either Identity Request (5GMMIdentityRequest) or Authentication request
        (5GMMAuthenticationRequest)
        """
        if recv_msg_name == '5GMMAuthenticationRequest':
            if 'AUTN' not in MsgRecvdDict:
                error_message = "5GMMAuthenticationRequest did not contain AUTN"
                return FGMMState.FAIL, error_message
        # TODO: Add elif for 5GMMIdentityRequest
        else:
            error_message = f"Expected 5GMMAuthenticationRequest but got {recv_msg_name}"
            return FGMMState.FAIL, error_message
    elif PrevMsgSent._name == '5GMMAuthenticationResponse':
        if recv_msg_name == '5GMMSecurityModeCommand':
            return FGMMState.NULL, None
        # Note: didn't handle the compliance test to show results
        else:
            error_message = f"Expected 5GMMSecurityModeCommand but got {recv_msg_name}"
            return FGMMState.FAIL, error_message
    elif PrevMsgSent._name == '5GMMSecurityModeComplete':
        """
        During the registration procedure, after sending the 5GMMSecurityModeCommand the UE
        should received the 5GMMRegistrationAccept response.
        """
        if recv_msg_name != '5GMMRegistrationAccept':
            """ Check if we didn't send an invalid request for compliance test """
            if PrevMsgSentDict.get('NASContainer').get('V') and PrevMsgSentDict['NASContainer']['V'] == b'\x00\x00':
                """ We sent an invalid 5GMMSecurityModeComplete with no UE data
                we should get a registration reject
                """
                if recv_msg_name != '5GMMRegistrationReject':
                    error_message = f"Expected 5GMMRegistrationReject but got {recv_msg_name}"
                    return FGMMState.FAIL, error_message
                # We expected reject therefore pass
                return FGMMState.PASS, None
            else:
                error_message = f"Expected 5GMMRegistrationAccept but got {recv_msg_name}"
                return FGMMState.FAIL, error_message
    # elif PrevMsgSent._name == '5GSMPDUSessionEstabRequest':

    elif PrevMsgSent._name == '5GMMMODeregistrationRequest':
        """ UE-initiated Deregistration procedure 3GPP TS 23.502 4.2.2.3.2

        The next message from the CN should be De-registration Accept (5GMMMODeregistrationAccept)
        """
        if recv_msg_name == '5GMMMODeregistrationAccept':
            if '5GMMCause' in MsgRecvdDict:
                error_message = f"5GMMMODeregistrationComplete contained RejectionCause: {MsgRecvdDict['RejectionCause']}"
                return FGMMState.FAIL, error_message
        else:
            error_message = f"Expected 5GMMMODeregistrationAccept but got {recv_msg_name}"
            return FGMMState.FAIL, error_message
    elif recv_msg_name == '5GMMANConnectionReleaseComplete':
        # Check if we received 5GMMMODeregistrationAccept
        if PrevMsgSent._name == '5GMMMODeregistrationAccept':
            return FGMMState.PASS, None
        else:
            error_message = f"Expected 5GMMMODeregistrationAccept but got 5GMMANConnectionReleaseComplete"
            return FGMMState.FAIL, error_message

    return FGMMState.NULL, None


g_verbose = 0
start_time = 0


class UE:
    def __init__(self, config=None):
        """
        Initializes a new UE object with the given configuration.

        Args:
            config (dict): A dictionary containing the configuration data for the UE.
                Must have the keys 'mmn' and 'supi'.

        Returns:
            None
        """
        global logger
        self.common_ies = self.create_common_ies()

        # Set map for compliance flows, used if program in compliance check mode
        self.compliance_mapper = {}

        # Set several instance variables to None
        self.ue_capabilities = self.ue_security_capabilities = self.ue_network_capability = None
        self.MsgInBytes = None
        self.RcvMsgInBytes = None
        self.IpAddress = None
        self.CiphAlgo = None
        self.IntegAlgo = None
        self.start_time = None
        self.end_time = None
        self.state = FGMMState.NULL
        self.procedure_times = {}
        # Set values for empty variables to all zeros in bytes
        empty_values = ['k_nas_int', 'k_nas_enc', 'k_amf', 'k_ausf', 'k_seaf', 'sqn', 'autn',
                        'mac_a', 'mac_s', 'xres_star', 'xres', 'res_star', 'res', 'rand']
        for var_name in empty_values:
            setattr(self, var_name, b'\x00' * 32)

        self.supi = self.amf_ue_ngap_id = None
        self.procedure = None  # contains the request that UE is processing or has
        self.error_message = ""
        self.current_procedure = 0
        self.procedures = config.get('procedures') if 'procedures' in config else [
            '5GMMRegistrationRequest', '5GMMMODeregistrationRequest']
        if config is None:
            # raise ValueError(f"Config is required")
            # If config is None, set some variables to None and others to default values
            self.op_type, self.state_time = 'OPC', time.time()
        else:
            # Otherwise, set variables based on values from config
            # The elements on procedures should be keys in request_mapper
            self.supi = config['supi']
            self.mcc = config['mcc']
            self.mnc = config['mnc']
            self.msin = config['supi'][-10:]
            self.key = config['key']
            self.op = config['op']
            self.op_type = config['opType']
            self.amf = config['amf']
            self.imei = config['imei']
            self.imeiSv = config['imeiSv']
            sn_name = "5G:mnc{:03d}.mcc{:03d}.3gppnetwork.org".format(
                int(config['mnc']), int(config['mcc']))
            self.sn_name = sn_name.encode()
            self.nssai = [{'SST': int(a['sst']), 'SD': int(a['sd'])}
                          # Create dictionaries for each item in defaultNssai list
                          if 'sd' in a else {'SST': int(a['sst'])}
                          for a in config['defaultNssai']]
            self.state_time = time.time()

    def set_k_nas_int(self, k_nas_int):
        self.k_nas_int = k_nas_int

    def set_procedure(self, code):
        self.procedure_times[code] = time.time()

    def set_state(self, state):
        self.state = state
        self.state_time = time.time()

    def set_compliance_mapper(self, mapper):
        self.compliance_mapper = mapper

    # 该函数用于根据接收到的消息确定下一步要执行的处理程序。它接收一个消息对象或字节串，
    # 并根据消息类型和当前状态选择相应的处理函数，然后调用该函数并返回处理结果。
    def next_action(self, Msg, msg_type=None):
        """
        Determines the next procedure to process based on the given response.

        Args:
            response: The response received by the UE.
                Should be a string representing the current procedure being processed.

        Returns:
            The function corresponding to the procedure to be processed next.
        """
        # 如果全局变量 g_verbose 的值大于等于3且 Msg 不为空，则调用 validator 函数进行验证
        if g_verbose >= 3 and Msg is not None:
            validator(self.MsgInBytes, Msg)

        # 如果 Msg 不是字节串并且其类型为 '5GMMSecProtNASMessage'，
        # 则调用 security_prot_decrypt 函数对其进行解密。
        if type(Msg) is not bytes:
            DecryptMsg = None
            if Msg != None and Msg._name == '5GMMSecProtNASMessage':
                DecryptMsg = security_prot_decrypt(Msg, self)
            # logger.debug("|----------------------------------------------------------------------------------------------------------------|")
            logger.debug(f"\n|----------------------------------------------------------------------------------------------------------------|\n\
            UE {self.supi} received message\n\
|----------------------------------------------------------------------------------------------------------------|\n\
\n{DecryptMsg.show() if DecryptMsg != None else Msg.show() if Msg != None else None}\n\
|----------------------------------------------------------------------------------------------------------------|\n\n")

        # Get the procedure function corresponding to the given response
        # 初始化 IEs 和 action_func 变量。如果提供了 Msg 和 msg_type，
        # 则从 response_mapper 中获取对应的处理函数。
        IEs = {}
        action_func = None
        if Msg and msg_type:
            action_func = response_mapper.get(msg_type)

        # 如果没有找到处理函数，则根据当前步骤在 procedures 列表中的索引，
        # 选择下一个步骤的处理函数。如果已经是最后一个步骤，则返回特定的结束消息。
        if action_func is None:
            # Get the index of the current procedure in procedures
            idx = self.procedures.index(
                self.procedure) if self.procedure in self.procedures else -1
            # Get the next procedure in procedures (wrapping around if necessary)
            if (idx + 1) >= len(self.procedures):
                return None, self, "5GMMANConnectionReleaseComplete"
            # procedure = self.procedures[(idx + 1) % len(self.procedures)]
            procedure = self.procedures[idx + 1]
            # Get the procedure function corresponding to the next procedure
            action_func = request_mapper[procedure]
            # Update the UE's state with the next procedure
            self.procedure = procedure

        # Call the procedure function and return its result

        # 调用确定的处理函数，并根据返回的消息类型判断是否需要进一步处理。
        # 如果消息类型为 '5GSMPDUSessionTransmission'，则直接返回。
        Msg, sent_type = action_func(self, IEs, Msg)
        if sent_type == '5GSMPDUSessionTransmission':  # Already in bytes
            return Msg, self, sent_type

        # 如果消息类型为 '5GMMSecProtNASMessage'，则调用 parse_NAS5G 函数解析消息。
        DecryptMsg = None
        if Msg != None and Msg._name == '5GMMSecProtNASMessage':
            DecryptMsg, e = parse_NAS5G(Msg._dec_msg)
        logger.debug(f" \n|----------------------------------------------------------------------------------------------------------------|\n\
        UE {self.supi} sending message \n\
|----------------------------------------------------------------------------------------------------------------|\n\
\n{DecryptMsg.show() if DecryptMsg != None else Msg.show() if Msg != None else None} \n\
|----------------------------------------------------------------------------------------------------------------|\n\n")
        # 记录即将发送的消息详细信息，包括解密后的消息内容或原始消息内容。
        ReturnMsg = Msg.to_bytes() if Msg != None else None
        return ReturnMsg, self, sent_type

    def next_compliance_test(self, Msg, type=None):
        if g_verbose > 3 and Msg is not None:
            self.RcvMsgInBytes = Msg.to_bytes() if Msg != b'F' else None
            logger.debug(f"UE {self.supi} received {type}")
            test_result, error_message = validator(self.MsgInBytes, Msg)
            if test_result != None:
                # We have reached end of test.
                # Validator return PASS on an expected reject is received or when succcessfully deregistered and connection release
                # It returns None otherwise
                self.error_message = error_message
                return None, self, None

        IEs = {}
        action_func = None
        if Msg and type:
            action_func = self.compliance_mapper.get(type)
            # action_func = response_mapper.get(type)

        if action_func is None:
            # Get the index of the current procedure in procedures
            idx = self.procedures.index(
                self.procedure) if self.procedure in self.procedures else -1
            # Get the next procedure in procedures (wrapping around if necessary)
            if (idx + 1) >= len(self.procedures):
                return None, self, None
            # procedure = self.procedures[(idx + 1) % len(self.procedures)]
            procedure = self.procedures[idx + 1]
            # Get the procedure function corresponding to the next procedure
            action_func = self.compliance_mapper[procedure]
            # Update the UE's state with the next procedure
            self.procedure = procedure

        # Call the procedure function and return its result
        Msg, sent_type = action_func(self, IEs, Msg)
        logger.debug(f"UE {self.supi} sending message \n{Msg.show() if Msg != None else None}")
        return Msg.to_bytes() if Msg != None else None, self, sent_type

    def create_common_ies(self):
        IEs = {}
        IEs['NAS_KSI'] = {'TSC': 0, 'Value': 7}
        return IEs

    def __str__(self):
        return "<UE supi={}, mcc={}, mnc={}, imei={}>".format(self.supi, self.mcc, self.mnc, self.imei)

    def __repr__(self) -> str:
        return (f'UE( SUPI: {self.supi}, AMF UE NGAP ID: '
                f'{self.amf_ue_ngap_id}, k_nas_int: {hexlify(self.k_nas_int)}, '
                f'k_nas_enc: {hexlify(self.k_nas_enc)}, k_amf: {hexlify(self.k_amf)}, '
                f'k_ausf: {hexlify(self.k_ausf)}, k_seaf: {hexlify(self.k_seaf)}, '
                f'k_nas_int: {hexlify(self.k_nas_int)}, k_nas_enc: {hexlify(self.k_nas_enc)} )')

    def __format__(self, format_spec: str) -> str:
        return (f'UE( SUPI: {self.supi}, AMF UE NGAP ID: '
                f'{self.amf_ue_ngap_id}, k_nas_int: {hexlify(self.k_nas_int)}, '
                f'k_nas_enc: {hexlify(self.k_nas_enc)}, k_amf: {hexlify(self.k_amf)}, '
                f'k_ausf: {hexlify(self.k_ausf)}, k_seaf: {hexlify(self.k_seaf)}, '
                f'k_nas_int: {hexlify(self.k_nas_int)}, k_nas_enc: {hexlify(self.k_nas_enc)} )')