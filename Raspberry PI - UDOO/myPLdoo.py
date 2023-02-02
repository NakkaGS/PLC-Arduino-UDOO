from snap7.snap7types import *
from snap7.util import *
import time
from random import *

ON = 1
OFF = 0

def ReadInput(plc, bit):
    area = 0x81  #area da memoria I
    start = 0  #localizacao de onde comeca a ler - Istart.bit
    length = 1  #tamanho dos dados da leitura - 1 bit

    result = plc.read_area(area, 0, start, length)

    if bit >= 0:
        return get_bool(result, 0, bit)
    else:
        return None


def ReadOutput(plc, bit):
    area = 0x82  #area da memoria Q
    start = 0  #localizacao de onde comeca a ler - Qstart.bit
    length = 1  #tamanho dos dados da leitura - 1 bit

    result = plc.read_area(area, 0, start, length)

    if bit >= 0:
        return get_bool(result, 0, bit)
    else:
        return None


def WriteOutput(plc, bit, value):
    area = 0x82  #area da memoria Q
    start = 0  #localizacao de onde comeca a ler - Qstart.bit
    length = 1  #tamanho dos dados da leitura - 1 bit

    result = plc.read_area(area, 0, start, length)

    if bit >= 0:
        set_bool(result, 0, bit, value)
    plc.write_area(0x82, 0, start, result)


def ReadMemory(plc, bit, pos):  #Mpos.bit
    area = 0x83  #area da memoria Q M-bit/MW-word
    length = 1  #tamanho dos dados da leitura - pode ser bit/word/double_word

    result = plc.read_area(area, 0, pos, length)

    if bit >= 0:
        return get_bool(result, 0, bit)
    else:
        return None


def WriteMemory(plc, bit, pos, value):
    area = 0x83  #area da memoria Q M-bit/MW-word
    length = 1 #tamanho dos dados da leitura - pode ser bit/word/double_word

    result = plc.read_area(area, 0, pos, length)

    if bit >= 0:
        set_bool(result, 0, bit, value)
    plc.write_area(area, 0, pos, result)


def Animation_1(plc, LED_UM, LED_DOIS, LED_TRES, LED_QUATRO, LED_CINCO):
    WriteOutput(plc, LED_UM, ON)
    WriteOutput(plc, LED_DOIS, OFF)
    WriteOutput(plc, LED_TRES, OFF)
    WriteOutput(plc, LED_QUATRO, OFF)
    WriteOutput(plc, LED_CINCO, OFF)
    time.sleep(.100)
    WriteOutput(plc, LED_UM, OFF)
    WriteOutput(plc, LED_DOIS, ON)
    WriteOutput(plc, LED_TRES, OFF)
    WriteOutput(plc, LED_QUATRO, OFF)
    WriteOutput(plc, LED_CINCO, OFF)
    time.sleep(.100)
    WriteOutput(plc, LED_UM, OFF)
    WriteOutput(plc, LED_DOIS, OFF)
    WriteOutput(plc, LED_TRES, ON)
    WriteOutput(plc, LED_QUATRO, OFF)
    WriteOutput(plc, LED_CINCO, OFF)
    time.sleep(.100)
    WriteOutput(plc, LED_UM, OFF)
    WriteOutput(plc, LED_DOIS, OFF)
    WriteOutput(plc, LED_TRES, OFF)
    WriteOutput(plc, LED_QUATRO, ON)
    WriteOutput(plc, LED_CINCO, OFF)
    time.sleep(.100)
    WriteOutput(plc, LED_UM, OFF)
    WriteOutput(plc, LED_DOIS, OFF)
    WriteOutput(plc, LED_TRES, OFF)
    WriteOutput(plc, LED_QUATRO, OFF)
    WriteOutput(plc, LED_CINCO, ON)
    time.sleep(.100)
    WriteOutput(plc, LED_UM, OFF)
    WriteOutput(plc, LED_DOIS, OFF)
    WriteOutput(plc, LED_TRES, OFF)
    WriteOutput(plc, LED_QUATRO, ON)
    WriteOutput(plc, LED_CINCO, OFF)
    time.sleep(.100)
    WriteOutput(plc, LED_UM, OFF)
    WriteOutput(plc, LED_DOIS, OFF)
    WriteOutput(plc, LED_TRES, ON)
    WriteOutput(plc, LED_QUATRO, OFF)
    WriteOutput(plc, LED_CINCO, OFF)
    time.sleep(.100)
    WriteOutput(plc, LED_UM, OFF)
    WriteOutput(plc, LED_DOIS, ON)
    WriteOutput(plc, LED_TRES, OFF)
    WriteOutput(plc, LED_QUATRO, OFF)
    WriteOutput(plc, LED_CINCO, OFF)
    time.sleep(.100)
    WriteOutput(plc, LED_UM, ON)
    WriteOutput(plc, LED_DOIS, OFF)
    WriteOutput(plc, LED_TRES, OFF)
    WriteOutput(plc, LED_QUATRO, OFF)
    WriteOutput(plc, LED_CINCO, OFF)
    time.sleep(.350)


def Animation_2(plc, LED_UM, LED_DOIS, LED_TRES, LED_QUATRO, LED_CINCO):
    for x in range(20):
        led_on = randint(0, 4)
        led_off = randint(0, 4)
        WriteOutput(plc, led_on, ON)
        WriteOutput(plc, led_off, OFF)
        time.sleep(.200)

def turnAllOFF(plc, LED_UM, LED_DOIS, LED_TRES, LED_QUATRO, LED_CINCO):
    WriteOutput(plc, LED_UM, OFF)
    WriteOutput(plc, LED_DOIS, OFF)
    WriteOutput(plc, LED_TRES, OFF)
    WriteOutput(plc, LED_QUATRO, OFF)
    WriteOutput(plc, LED_CINCO, OFF)

