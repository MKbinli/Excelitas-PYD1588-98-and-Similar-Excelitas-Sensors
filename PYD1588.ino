//#include <Time.h>

int pinSL = 16;
int pinDL = 17;
unsigned long pirConfigVal = 0x10;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(pinSL, OUTPUT);
  digitalWrite(pinSL, LOW);
  pinMode(pinDL, OUTPUT);
  digitalWrite(pinDL, LOW);

  while (!Serial) {
    ;
  }
  congfigSensor();
  pinMode(pinDL, INPUT);
  delayMicroseconds(3000);
  
 
}

void congfigSensor(){
  unsigned long regmask = 0x1000000;
  delay(1);
  configVal=pirConfigVal;
  bitCount = 25
  for (int i=0;i<25,i++){
    bit = (configVal&regmask)!=0;
    regmask >>= 1;
    digitalWrite(pinSL, LOW);
    digitalWrite(pinSL, HIGH);
    if(bit){
      digitalWrite(pinSL, HIGH);
    }
    else{
      digitalWrite(pinSL, LOW);
    }
    delayMicroseconds(100); 
  }
  digitalWrite(pinSL, LOW);
  delayMicroseconds(650);
}

void readSensorVal(){
  
  int fixedBitSize=15;
  int fixedBitSizeConfig=25;
  unsigned long uibitmask = 0x4000;
  int PIRval = 0; // PIR signal
  unsigned long statcfg = 0; 

  digitalWrite(pinDL, HIGH);
  pinMode(pinDL, OUTPUT);
  delayMicroseconds(140);
  for(int i=0, i<fixedBitSize,i++){
    digitalWrite(pinDL, LOW);
    pinMode(pinDL, OUTPUT);
    digitalWrite(pinDL, HIGH);
    pinMode(pinDL, INPUT);
    delayMicroseconds(3);
    if(digitalRead(pinDL)){
      PIRval |= uibitmask;
    }
    uibitmask>>=1;
    
  }
  uibitmask = 0x1000000;
  statcfg = 0;
  for (i=0; i < 25; i++)
  { 
    digitalWrite(pinDL, LOW);
    pinMode(pinDL, OUTPUT);
    digitalWrite(pinDL, HIGH);
    pinMode(pinDL, INPUT);
    delayMicroseconds(3);
    if(digitalRead(pinDL)){
      statcfg |= uibitmask;
    }
    uibitmask>>=1;
  }
  digitalWrite(pinDL, LOW);
  pinMode(pinDL, OUTPUT);
  delayMicroseconds(160);
  pinMode(pinDL, INPUT);
  Serial.println(PIRval);
  Serial.println(PIRval,BIN);
  Serial.println(PIRval,HEX);
  Serial.println(statcfg);
  Serial.println(statcfg,BIN);
  Serial.println(statcfg,HEX);
  delay(3000);
}

void loop() {
  readSensorVal();
}
