import MySQLdb
import string
import serial
import struct

#####################################################################
#FUNCAO PARA VER SE O SENSOR EH DIGITAL OU ANALOGICO
def d_ou_a(device_id):

  if any([device_id == '1' or device_id == '2' or device_id == '5' or device_id == '6']):
	  tipo_sensor = 1
	  return tipo_sensor

  if any([device_id ==  '3' or device_id == '4' or device_id == '7' or device_id == '8']):
	  tipo_sensor = 2
	  return tipo_sensor
 

#####################################################################
#FUNCAO PARA ENVIAR O VALOR DO SENSOR PARA O BANCO DE DADOS
def envia_db(device_id, valor, digitalanalog):

	#Configura os dados do banco de dados
	SERVERNAME = 'localhost' 
	USERNAME = 'root' 
	PASSWORD = 'udooer'
	DATABASE = 'nkt_tcc'

	#Conecta com MySQL usando a biblioteca MySQLdb
	db = MySQLdb.connect(SERVERNAME,USERNAME,PASSWORD,DATABASE)
	cursor = db.cursor()

	#Caso seja digital ele manda para digital_data/digital_value
	if (digitalanalog == 1): #eh digital
		try:
			cursor.execute("""INSERT INTO digital_data(device_id, digital_value) VALUES (%s,%s)""",(device_id,valor))	
			db.commit()
			imprimir_result(device_id, valor, digitalanalog)
		except:     
			db.rollback()

	#Caso seja analogico ele manda para analog_data/analog_value
	if (digitalanalog == 2): #eh analogico
		try:
			cursor.execute("""INSERT INTO analog_data(device_id, analog_value) VALUES (%s,%s)""",(device_id,valor))	
			db.commit()
			
			imprimir_result(device_id, valor, digitalanalog)

		except:
			print "\n--ERRO NA GRAVACAO--\n"     
			db.rollback()


#####################################################################
#FUNCAO PARA ADICIONAR OS TEXTO INICIAL
def texto_inicial():

	print "\n#############################################"
	print "#  Sistema MyArdoo - Gabriel Nakata 2017/2  #"
	print "#                 Iniciar                   #"
	print "############################################"


#####################################################################
#DEFINE O TIPO DE SENSOR E PREPARA OS DADOS PARA ENVIAR PARA O BANCO DE DADOS
def prepara_sensor(sensor, valor):
    #Define se o sensor eh digital ou analogico
    type_sensor = d_ou_a(sensor)

    #Envia para o banco de dados
    envia_db(sensor, valor, type_sensor) 


#####################################################################
#VERIFICA QUAIS SENSORES ESTAO ATIVOS
def sensores_input(data, tamanho):
  #Sensor 1 - Arduino - Digital - Input
  if(data[0] and data[1] > -1):
    sensor_1 = data[0]
    value_1 = data[1] 
    prepara_sensor(sensor_1, value_1)


  #Sensor 3 - Arduino - Analogico - Input
  if (data[2] and data[3] > -1):
    sensor_3 = data[2]
    value_3 = data[3] 
    prepara_sensor(sensor_3, value_3)


  #Sensor 5 - CLP - Digital - Input
  if (data[4] and data[5] > -1):
    sensor_5 = data[4]
    value_5 = data[5] 
    prepara_sensor(sensor_5, value_5)

    
  #Sensor 7 - CLP - Analogico - Input
  if (data[6] and data[7] > -1):
    sensor_7 = data[6]
    value_7 = data[7] 
    prepara_sensor(sensor_7, value_7)


#####################################################################
#DISTRIBUI OS VALORES E SENSORES
def organizar_leitura(ardoo, dado):
  #Le uma linha da serial
  reading = ardoo.readline()
  #Separa os dados por #
  base = string.split(reading,"#")

  #Deixa todos os valores do vetor dado igual a -1
  for i in range(len(base)):
    dado.append(-1)

  #Distribui os sensores disponiveis e seus valores
  for i in range(len(base)):
    dado[i] = base[i]

  return dado

#####################################################################
#IMPRIME OS DADOS GRAVADOS
def imprimir_result(id_sensor, valor_sensor, umdois):

  print "\n--RECEBEU DO BANCOS DE DADOS--"
  print "Sensor ID = "+id_sensor	
  print "Valor = "+valor_sensor

  #Nomeio se eh digital ou analogico
  if umdois == 1:
	tipo = 'Digital' 
  else: 
	tipo = 'Analogico'


  print "Tipo = " +tipo[::]
  

#####################################################################
#ENVIA DADOS PARA A SERIAL
def envia_dados(ardoo, sensor_id, valor_sensor):
  ardoo.write(struct.pack('>BB',sensor_id,valor_sensor))

  print "\n--ENVIOU PARA SERIAL--"
  print "Sensor ID = %d" % (sensor_id)  
  print "Valor = %d" % (valor_sensor)


#####################################################################
#FUNCAO PARA RECEBER DO BANCO DE DADOS PARA ENVIAR PARA A SERIAL
def recebe_db(ardoo, deviceID):

  #Configura os dados do banco de dados
  SERVERNAME = 'localhost' 
  USERNAME = 'root' 
  PASSWORD = 'udooer'
  DATABASE = 'nkt_tcc'

  #Conecta com MySQL usando a biblioteca MySQLdb
  db = MySQLdb.connect(SERVERNAME,USERNAME,PASSWORD,DATABASE)
  cursor = db.cursor()

  #Caso seja digital ele manda para digital_data/digital_value
  if (deviceID == 2 or deviceID == 6): #eh digital
    try:
      cursor.execute("SELECT digital_value FROM digital_data  WHERE device_id = %d ORDER BY digital_id DESC LIMIT 1" % (deviceID))
      resultado = cursor.fetchall()
      for row in resultado:
        valor = row[0]
      valor_enviar = int(valor)
      envia_dados(ardoo, deviceID, valor_enviar)   
    except:
      print "\n--ERRO NA GRAVACAO - DIGITAL--\n"  


  #Caso seja analogico ele manda para analog_data/analog_value
  if (deviceID == 4 or deviceID == 8): #eh analogico
    try:
      cursor.execute("SELECT analog_value FROM analog_data  WHERE device_id = %d ORDER BY analog_id DESC LIMIT 1" % (deviceID))
      resultado = cursor.fetchall()
      for row in resultado:
        valor = row[0]
      valor_enviar = int(valor)
      envia_dados(ardoo, deviceID, valor_enviar) 

    except:
      print "\n--ERRO NA GRAVACAO - ANALOGICO--\n"     
      db.rollback()

  db.close()
  