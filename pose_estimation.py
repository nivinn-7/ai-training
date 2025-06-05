import mediapipe as mp
import cv2
import winsound
import smtplib
import ssl
from email.message import EmailMessage
import time
import os

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
email_sent = False

def send_email_with_attachment(image_path):
    sender_email = "mca2445@rajagiri.edu"
    receiver_email = "mca2445@rajagiri.edu"
    password = "xjks rfhv xdpo wmfd"  # Use App Password if 2FA is enabled

    msg = EmailMessage()
    msg["Subject"] = "🚨 Intruder Alert - Human Detected"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("A human was detected. See attached screenshot.")

    with open(image_path, "rb") as img:
        img_data = img.read()
        msg.add_attachment(img_data, maintype="image", subtype="jpeg", filename="intruder.jpg")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    if results.pose_landmarks:
        cv2.putText(frame, f'Human detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        winsound.Beep(1000,300)
        if not email_sent:
            timestamp = int(time.time())
            img_path = f"intruder_{timestamp}.jpg"
            cv2.imwrite(img_path, frame)
            send_email_with_attachment(img_path)
            os.remove(img_path)
            email_sent = True

    cv2.imshow('Pose Estimation', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()