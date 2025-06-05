import cv2
import pyttsx3

from deepface import DeepFace

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
cap=cv2.VideoCapture(0)
while True:
    ret,img = cap.read()
    results = DeepFace.analyze(img,actions=['emotion'],enforce_detection=False)
    emotion = results[0]['dominant_emotion']
    cv2.putText(img,f'Emotion:{emotion}',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    engine.say(emotion)
    engine.runAndWait()
    cv2.imshow("Emotion Recognition",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()