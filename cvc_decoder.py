#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mmap
from bitstring import BitArray

fdlist = []

with open(os.path.join(os.getcwd(), "result"), "r+b") as input_file:
    mm = mmap.mmap(input_file.fileno(), 0)
    packetcnt = mm.size() // (1024 - 128)
    for i in range(packetcnt):
        mm.read(4)  # пропустили заголовок
        body = BitArray(mm.read(1020 - 128))

        # разбор заголовка транспортного кадра (virtual channel data unit, VCDU)
        ver = body[0:2]  # Номер версии
        scid = body[2:10]  # Номер КА, присваиваемый CCSDS
        vcid = body[10:16]  # Идентификатор виртуального канала (определяет принадлежность данных)
        # чтобы можно было выводить vcid в шестнадцатеричном представлении дополнили его до числа разрядов кратных 4-м
        vcid.prepend("0b00")
        vcducnt_1 = body[16:40]  # счетчик виртуальных кадров
        rf = body[40:41]  # флаг воспроизведения (0 - для данных, поступающих в режиме РВ, 1 - для данных с ЗУ
        # зарезервировано (spare) 7 bits
        # вторичный заголовок (присутствует в первом пакете)
        vcducnt_2 = body[48:56]
        key = body[56:72]  # ключ шифрования (encryption key)
        # зарезервировано (spare) 8 bits
        print("ver:", ver.bin, "scid:", scid.hex, "vcid:", vcid, "vcducnt:", vcducnt_1, "rf:", rf.bin)

        # чтение поля данных транспортного уровня
        vcdudata = body[80:7136]

        '''
        svid = scid + vcid
        if os.path.isfile(os.path.join(os.getcwd(), str(svid))):
            # добавляем VCDU Data Zone
            pass
        else:
            fd = open(str(svid), "w+b")
            # fdlist[str(svid): pickle.dumps(fd)]
            fdlist.append(fd)
            fl = fd[1]
            fl.close()
        break
        '''
