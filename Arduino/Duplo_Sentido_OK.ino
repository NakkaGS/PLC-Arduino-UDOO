#include <myArdoo.h>

myArdoo udoo;

#define NUM_SENSOR_OUT 4

int sensoresOut = udoo.qtd_dados(NUM_SENSOR_OUT);
int recebendo[NUM_SENSOR_OUT];

int led = 13;

void setup() {
  Serial.begin(115200);
  pinMode(led,OUTPUT);

}

void loop() {
  //Saidas
  udoo.ler_serial(recebendo, sensoresOut);

  int sensor2 = udoo.valor_sensor(recebendo, 2); //Arduino - Digital
  int sensor4 = udoo.valor_sensor(recebendo, 4); //Arduino - Analogico
  int sensor6 = udoo.valor_sensor(recebendo, 6); //CLP - Digital
  int sensor8 = udoo.valor_sensor(recebendo, 8); //CLP - Analogico
  
  if(sensor2 == 1 && sensor6== 1){
    digitalWrite(led, HIGH);
  }else{
    digitalWrite(led,LOW);
  }
  
  delay(1000);

  //Entradas
  for(int i = 0; i <15; i++){
    udoo.escrever_serial(1,i);
    udoo.escrever_serial(3,i+4); //Arduino - Analogico
    udoo.escrever_serial(5,i*2); //CLP - Digital
    udoo.escrever_serial(7,i*9);
    udoo.fechar_serial();
  }
}
