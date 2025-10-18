import cv2
import mediapipe as mp
import pygame
import os

pygame.mixer.init()

sound_path = "seyuh-carti.mp3" 
if not os.path.exists(sound_path):
    raise FileNotFoundError(f"Sound file not found: {sound_path}")
sound = pygame.mixer.Sound(sound_path)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

# State tracking
sound_playing = False

def fingers_up(hand_landmarks):
    lm = hand_landmarks.landmark
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb (right hand assumption)
    if lm[tip_ids[0]].x < lm[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for id in range(1, 5):
        if lm[tip_ids[id]].y < lm[tip_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    matched = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers = fingers_up(hand_landmarks)

            if fingers == [1, 1, 1, 0, 0]:  # Thumb, Index, Middle
               # cv2.rectangle(frame, (100, 50), (300, 200), (0, 0, 0), 3)
                cv2.putText(frame, "Seeyah!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1.2, (0, 0, 0), 3)
                matched = True

                if not sound_playing:
                    sound.play(-1)  
                    sound_playing = True

                break

    if not matched:
        cv2.putText(frame, "FAWH no fingers detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2)
        if sound_playing:
            sound.stop()
            sound_playing = False

    cv2.imshow("SEEYAH", frame)

    if cv2.waitKey(1) == 27:  # ESC
        break

sound.stop()
cap.release()
cv2.destroyAllWindows()
