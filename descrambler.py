#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mmap
from bitstring import BitArray

# нумерация  в BitArray идет от старшего бита (0) к младшему (length - 1)!

def gamma_generator(n):
    """
    Генератор гаммы
    :param n: размер гаммы в битах
    :return: гамма
    """
    x = BitArray("0b11111111")  # начальное значение генератора гаммы
    gamma = BitArray()
    for i in range(n):
        gamma.append(bin(x[7]))  # добавили очередной бит к гамме
        mask = x[7] ^ x[4] ^ x[2] ^ x[0]  # сформировали старший разряд маски
        x.ror(1)
        x.set(mask, 0)
    return gamma


'''
with open(os.path.join(os.getcwd(), "data"), "r+b") as fd:
    unscrambled_data = BitArray(fd.read())
    scrambled_data = unscrambled_data ^ gamma_generator(unscrambled_data.length)

with open(os.path.join(os.getcwd(), "result"), "w+b") as fd:
    fd.write(scrambled_data.bytes)
'''

gamma = gamma_generator((1020 - 128) * 8)  # размер в битах
output_file = open(os.path.join(os.getcwd(), "result"), "w+b")
with open(os.path.join(os.getcwd(), "NOAA-20.raw"), "r+b") as input_file:
    mm = mmap.mmap(input_file.fileno(), 0)
    while True:
        index = mm.find(b'\x1a\xcf\xfc\x1d')
        if index == -1:
            break
        mm.seek(index)
        print("index", hex(index))

        # читаем CADU вместе с заголовком, если заголовок не нужен, то предварительно mm.seek(index + 4)
        header = mm.read(4)
        unscrambled_body = BitArray(mm.read(1020 - 128))  # без 128 RS-symbols

        # дескремблируем тело CADU
        body = unscrambled_body ^ gamma

        # TODO: сделать проверку по кодам RS

        output_file.write(header + body.bytes)
output_file.close()

