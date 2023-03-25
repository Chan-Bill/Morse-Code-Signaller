int val;

void setup() 
{
  Serial.begin(9600); 
  pinMode(13, OUTPUT); 
  pinMode(12, OUTPUT); 
  pinMode(11, OUTPUT);
  digitalWrite (13, LOW);
  digitalWrite (12, LOW);
  digitalWrite (11, LOW);
}

void loop() {

  if (Serial.available() > 0){

    val = char(Serial.read())-'0';
    if(val == 0){
      digitalWrite (13, LOW);
      digitalWrite (12, LOW);
      digitalWrite (11, LOW);
      }
    if(val == 1){
      digitalWrite(13, HIGH);  
      }
    if(val == 2){
      digitalWrite(12, HIGH);
      }
    if(val == 3){
      digitalWrite(11, HIGH);
      }
    if(val == 4){
      digitalWrite(13, HIGH);
      digitalWrite(12, HIGH);
      }
    if(val == 5){
      digitalWrite(13, HIGH);
      digitalWrite(12, HIGH);
      digitalWrite(11, HIGH);
      }
  }

}
