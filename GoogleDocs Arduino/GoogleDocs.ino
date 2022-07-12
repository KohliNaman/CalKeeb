#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include "HTTPSRedirect.h"
#include "DebugMacros.h"


extern const char* ssid;
extern const char* password;
extern const char* host;
extern const char *GScriptId;

const int httpsPort = 443;
//#define GPIO_STATUS 2
const char* fingerprint = "";

String url2 = String("/macros/s/") + GScriptId + "/exec?cal";

HTTPSRedirect* client = nullptr;



void setup() {
  Serial.begin(9600);
  Serial.flush();
//  pinMode(GPIO_STATUS,OUTPUT);
//  digitalWrite(GPIO_STATUS,LOW);
  Serial.println();
  Serial.print("Connecting to wifi: ");
  Serial.println(ssid);
  
  Serial.flush();
//  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
//  digitalWrite(GPIO_STATUS,HIGH);
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  
   client = new HTTPSRedirect(httpsPort);
  client->setInsecure();
  client->setPrintResponseBody(true);
  client->setContentTypeHeader("application/json");
  
//  Serial.println("Connecting to ");
//  Serial.println(host);

  bool flag = false;
  for (int i=0; i<5; i++){
    int retval = client->connect(host, httpsPort);
    if (retval == 1) {
       flag = true;
       break;
    }
    else
      Serial.println("Connection failed. Retrying...");
  }

  if (!flag){
    Serial.println("Could not connect to server: ");
    Serial.println(host);
    Serial.println("Exiting...");
    return;
  }
  
//  Serial.println("\nGET: Fetch Google Calendar Data:");
//  Serial.println("================================");

  client->GET(url2, host);
  String lol = client->getResponseBody(); //bruh
//  Serial.println("lol");
  delete client;
  client = nullptr;

 
  delay(600000);
  
                          
}
