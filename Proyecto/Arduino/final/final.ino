#include <SPI.h>
#include <MFRC522.h>
#include <SoftwareSerial.h>

//#define esp Serial1
#define SS_PIN 10
#define RST_PIN 9

SoftwareSerial esp(2,3); // RX, TX

MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class

// Init array that will store new NUID
byte nuidPICC[4];


String CIPSTART  = {"AT+CIPSTART=\"TCP\",\"192.168.4.2\",8002\r\n"};

String device = "0";

String data;

String server = "192.168.4.2";

String uri = "/newLog";// our example is /esppost.php

byte dat [5];


void setup() {


  esp.begin(115200);

  Serial.begin(9600);

  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522


  Serial.println("Test");
  delay(2000);
  setWifi();
}

//reset the esp8266 module

void reset() {

  esp.println("AT+RST");

  delay(1000);

  if(esp.find("OK") ) Serial.println("Module Reset");
  else Serial.println("Failed");

}

//connect to your wifi network

void setWifi(){
  esp.println("AT+CWMODE=3");

  delay(1000);

  if(esp.find("OK") ){
    Serial.println("Paso 1");
    esp.println("AT+CWSAP=\"ESP\",\"password\",1,4");
    if(esp.find("OK") ){
      esp.println("AT+CIPAP=\"192.168.4.1\"");
      delay(500);
      if(esp.find("OK") ){
        Serial.println("Creado acces point");
        return;
      }
    }
  }
}

void loop () {

// Look for new cards
  if ( ! rfid.PICC_IsNewCardPresent())
    return;

  // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return;

  Serial.print(F("PICC type: "));
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
  Serial.println(rfid.PICC_GetTypeName(piccType));

  // Check is the PICC of Classic MIFARE type
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
    piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
    piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    Serial.println(F("Your tag is not of type MIFARE Classic."));
    return;
  }

  if (rfid.uid.uidByte[0] != nuidPICC[0] ||
    rfid.uid.uidByte[1] != nuidPICC[1] ||
    rfid.uid.uidByte[2] != nuidPICC[2] ||
    rfid.uid.uidByte[3] != nuidPICC[3] ) {
    Serial.println(F("A new card has been detected."));

    // Store NUID into nuidPICC array
    data="";
    for (byte i = 0; i < 4; i++) {
      nuidPICC[i] = rfid.uid.uidByte[i];
      data+=nuidPICC[i];
    }


  httppost();
    Serial.println(F("The NUID tag is:"));
    Serial.println(data);
  }
  else Serial.println(F("Card read previously."));

  // Halt PICC
  rfid.PICC_HaltA();

  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();
}

void httppost () {


  //esp.println("AT+CIPSTART=0,\"TCP\",\"google.com\",80");//start a TCP connection.
  //esp.println("AT+CIPSTART=\"TCP\",\"" + server + "\",3000");//start a TCP connection.
  Serial.println(CIPSTART);
  esp.println(CIPSTART);
  delay(6000);

  if( esp.find("OK")) {

    Serial.println("TCP connection ready");

  }


  delay(1000);

  int l = data.length() + device.length() + 13;

  String postRequest =

    "POST " + uri + " HTTP/1.0\r\n" +
    "Host: " + server + "\r\n" +
    "Content-Type: multipart/form-data\r\n" +
    "\r\n" +
    "Content-Disposition: form-data; name=\"picc\"\r\n" +
    data + "\r\n" + 
    "Content-Disposition: form-data; name=\"device\"\r\n" +
    device;

  Serial.println(postRequest);

  String sendCmd = "AT+CIPSEND=";//determine the number of caracters to be sent.

  esp.print(sendCmd);

  esp.println(postRequest.length() );

  if(esp.find(">")) {
    Serial.println("Sending.."); esp.print(postRequest);

    if( esp.find("SEND OK")) {
      Serial.println("Packet sent");

      while (esp.available()) {

        String tmpResp = esp.readString();

        Serial.println(tmpResp);

      }

      // close the connection

      esp.println("AT+CIPCLOSE");

    }

  }
  Serial.println("fin post");
}
