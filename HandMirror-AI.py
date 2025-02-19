import serial
import time
import cv2
import mediapipe as mp

# Configurazione della connessione seriale
esp32s3 = serial.Serial(port='COM3', baudrate=115200, timeout=1)
time.sleep(2)

# Configurazione di Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils

# Variabili per calcolare gli FPS
previousTime, currentTime = 0, 0

# Funzione per rilevare lo stato delle dita
def detect_fingers(image, hand_landmarks):
    finger_tips = [8, 12, 16, 20]  # Indice, Medio, Anulare, Mignolo
    thumb_tip = 4
    finger_states = [0, 0, 0, 0, 0]  # Pollice, Indice, Medio, Anulare, Mignolo

    # Rileva se il pollice è alzato
    if hand_landmarks.landmark[thumb_tip].x > hand_landmarks.landmark[thumb_tip - 1].x:
        finger_states[0] = 1

    # Rileva se le altre dita sono alzate
    for idx, tip in enumerate(finger_tips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[idx + 1] = 1  # Altre dita su

    return finger_states

# Apertura della videocamera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Preprocessamento dell'immagine
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Elaborazione delle mani rilevate
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_state = detect_fingers(image, hand_landmarks)

            # Invia lo stato delle dita alla porta seriale
            for state in fingers_state:
                esp32s3.write(bytes([state]))

            print(f"Fingers State: {fingers_state}")

    # Calcolo degli FPS
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    # Visualizzazione degli FPS sull'immagine
    cv2.putText(image, 'FPS ' + str(int(fps)), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Mostra il frame elaborato
    cv2.imshow('Hand Tracking', image)

    # Controllo per uscire dal ciclo con il tasto 'q'
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Rilascio delle risorse
cap.release()
cv2.destroyAllWindows()
esp32s3.close()
