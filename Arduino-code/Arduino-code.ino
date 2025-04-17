#include <ESP32Servo.h>  // Libreria per gestire i servo motori con l'ESP32

// Definizione dei pin GPIO a cui sono collegati i servo motori
int servoPins[] = {9, 10, 11, 12, 13};  // Pin per pollice, indice, medio, anulare, mignolo

// Creazione degli oggetti Servo per ogni dito
Servo servoThumb;  // Servo per il pollice
Servo servoIndex;  // Servo per l'indice
Servo servoMiddle; // Servo per il medio
Servo servoRing;   // Servo per l'anulare
Servo servoPinky;  // Servo per il mignolo

void setup() {
  // Inizializzazione della comunicazione seriale a 115200 baud
  Serial.begin(115200);

  // Collegamento di ogni servo al relativo pin GPIO
  servoThumb.attach(servoPins[0]);  // Collegamento del servo del pollice
  servoIndex.attach(servoPins[1]); // Collegamento del servo dell'indice
  servoMiddle.attach(servoPins[2]); // Collegamento del servo del medio
  servoRing.attach(servoPins[3]);   // Collegamento del servo dell'anulare
  servoPinky.attach(servoPins[4]);  // Collegamento del servo del mignolo

  // Inizializzazione dei servo alla posizione 0° (dita distese)
  servoThumb.write(0);
  servoIndex.write(0);
  servoMiddle.write(0);
  servoRing.write(0);
  servoPinky.write(0);
}

void loop() {
  // Controlla se sono disponibili almeno 5 byte nel buffer seriale
  if (Serial.available() >= 5) {
    // Lettura dello stato del pollice e aggiornamento del servo
    int fingerState = Serial.read(); // Lettura del valore per il pollice
    servoThumb.write(fingerState == 1 ? 90 : 0); // 90° per piegato, 0° per disteso

    // Lettura dello stato dell'indice e aggiornamento del servo
    fingerState = Serial.read(); // Lettura del valore per l'indice
    servoIndex.write(fingerState == 1 ? 90 : 0); // 90° per piegato, 0° per disteso

    // Lettura dello stato del medio e aggiornamento del servo
    fingerState = Serial.read(); // Lettura del valore per il medio
    servoMiddle.write(fingerState == 1 ? 90 : 0); // 90° per piegato, 0° per disteso

    // Lettura dello stato dell'anulare e aggiornamento del servo
    fingerState = Serial.read(); // Lettura del valore per l'anulare
    servoRing.write(fingerState == 1 ? 90 : 0); // 90° per piegato, 0° per disteso

    // Lettura dello stato del mignolo e aggiornamento del servo
    fingerState = Serial.read(); // Lettura del valore per il mignolo
    servoPinky.write(fingerState == 1 ? 90 : 0); // 90° per piegato, 0° per disteso
  }
}
