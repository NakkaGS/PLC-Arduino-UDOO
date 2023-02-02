import serial
import struct
import time
from myArdoo import *
from myPLdoo import *

import snap7.client as c
from snap7.snap7types import *

texto_inicial()

#############################################
#Configuracao da comunicao com o CLP

ON = 1
OFF = 0

LED_1 = 0
LED_2 = 1
LED_3 = 2
LED_4 = 3
LED_5 = 4

BOTTON_1 = 5
BOTTON_2 = 6
BOTTON_3 = 7 #Desliga
BOTTON_4 = 8
BOTTON_5 = 9 #Reset

KEY_1 = 0
KEY_2 = 1
KEY_3 = 2
KEY_4 = 3
KEY_5 = 4

plc = c.Client()
plc.connect('192.168.5.219', 0, 2)

#############################################
#Configuracao da comunicao com o Arduino

#Configura as porta e baud
SERIALPORT = '/dev/ttymxc3'
BAUDRATE = 115200

#Faz a conexao da serial do UDOO com o Arduino usando a porta /dev/ttymxc3
arduino = serial.Serial(SERIALPORT, BAUDRATE, timeout=10)
#############################################

time.sleep(0.5)

#counter = 0

while True:

  #ENTRADAS
  data = []

  while True:

    #SAIDAS
    #Escreve na serial a partir dos dados do banco de dados
    recebe_db(arduino,2) #Arduino - Digital
    recebe_db(arduino,4) #Arduino - Analogico
    recebe_db(arduino,6) #CLP - Digital
    recebe_db(arduino,8) #CLP - Analogico
  
    time.sleep(0.5)


    data = organizar_leitura(arduino, data)

    #Joga os dados do arduino no banco de dados
    sensores_input(data, len(data))

    if(Volta == 0):
      print 'Chave: %s - %s' %(ReadInput(plc, KEY_1),ReadInput(plc, KEY_2))
      time.sleep(.500)
      print ReadMemory(plc, 2, 0)
      if ReadInput(plc, KEY_5) == True:
          WriteMemory(plc, 1, 0, 1) #WriteMemory(plc, bit, pos, value)
      else:
          WriteMemory(plc, 1, 0, 0)
      if ReadInput(plc, BOTTON_3)== False: #Sai do while
          Volta = 1
          for x in range(10):
            if x%2==0:
              #Animation_1(plc, LED_1, LED_2, LED_3, LED_4, LED_5)
              Animation_2(plc, LED_1, LED_2, LED_3, LED_4, LED_5)
          break;




time.sleep(0.1) 




turnAllOFF(plc, LED_1, LED_2, LED_3, LED_4, LED_5)
plc.disconnect()