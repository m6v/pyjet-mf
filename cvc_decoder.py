#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mmap
from bitstring import BitArray   # см. https://pythonhosted.org/bitstring/bitarray.html


with open(os.path.join(os.getcwd(), "result"), "r+b") as input_file:
    mm = mmap.mmap(input_file.fileno(), 0)
    for i in range(40):
        mm.read(4)  # пропустили заголовок
        body = BitArray(mm.read(1020))
        # TODO: перепроверить побитную разбивку
        ver = body[0:2]
        scid = body[3:11]
        vcid = body[11:17]
        vcid.append("0b00")  # дополнили до числа разрядов кратных 4-м
        vcducnt_1 = body[18:42]
        replay_flag = body[43]
        # spare 7 bits
        vcducnt_2 = body[50:58]
        key = body[59:75]
        # spare 8 bits
        vcdudata = body[83:7056]
        print("ver:", ver, "scid:", scid.hex, "vcid:", vcid, "vcducnt_1:", vcducnt_1, "replay_flag:", bin(replay_flag),
              "vcducnt_2:", vcducnt_2.hex, "key:", key.hex)
