# Importazione delle librerie necessarie
import cv2              # Libreria per la computer vision
import mediapipe as mp  # Libreria per il rilevamento e il tracciamento delle mani
import time             # Libreria per la gestione del tempo

# Apertura della videocamera (id 0 per la videocamera predefinita)
camera = cv2.VideoCapture(0)

# Inizializzazione di Mediapipe per il rilevamento delle mani
mpHands = mp.solutions.hands         # Modulo per il rilevamento delle mani
hands = mpHands.Hands(               # Creazione dell'oggetto per il rilevamento delle mani
    static_image_mode=False,         # False per rilevare le mani in un flusso video continuo, True per immagini statiche
    max_num_hands=1,                 # Numero massimo di mani da rilevare nell'immagine
    min_detection_confidence=0.7,    # Soglia minima di confidenza per rilevare una mano
    min_tracking_confidence=0.7      # Soglia minima di confidenza per tracciare i punti di riferimento della mano
)
mpDraw = mp.solutions.drawing_utils  # Utilità per disegnare i punti di riferimento delle mani

# Variabili per il calcolo degli FPS (Frame Per Second)
previousTime = 0  # Tempo del frame precedente
currentTime = 0   # Tempo del frame corrente

# Ciclo principale per acquisire e processare i frame video
while True:
    success, img = camera.read()                   # Lettura del frame dalla videocamera
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Conversione del frame in RGB (richiesto da Mediapipe)
    results = hands.process(imgRGB)                # Elaborazione del frame per rilevare le mani

    # Se vengono rilevate mani, disegna i punti di riferimento e le connessioni
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Disegna i punti di riferimento delle mani sul frame originale
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # Calcolo degli FPS
    currentTime = time.time()               # Ottieni il tempo corrente
    fps = 1 / (currentTime - previousTime)  # FPS = 1 / (tempo tra i frame)
    previousTime = currentTime              # Aggiorna il tempo precedente

    # Visualizzazione degli FPS sul frame video
    cv2.putText(img, 'FPS ' + str(int(fps)), (10, 30),        # Testo da visualizzare
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)  # Font, dimensione, colore, spessore

    # Mostra il frame elaborato in una finestra
    cv2.imshow("Hand Tracking", img)

    # Interrompi il ciclo se l'utente preme il tasto "q"
    if cv2.waitKey(1) == ord("q"):
        break

# Rilascio della videocamera e chiusura delle finestre
camera.release()         # Libera le risorse della videocamera
cv2.destroyAllWindows()  # Chiude tutte le finestre create da OpenCV
