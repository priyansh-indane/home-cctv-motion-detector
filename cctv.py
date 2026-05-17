import cv2
import time
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# GMAIL settings
GMAIL_ADDRESS  = "<enter your gmail>"       # Your Gmail
APP_PASSWORD   = "<give gmail app password>"        # App password from Step 2
RECEIVER_EMAIL = "<give receiver gmail address>"       # Who gets the alert (can be same)
SENSITIVITY    = 3000   # Lower = more sensitive
COOLDOWN       = 30     # Seconds between alerts


def send_email_alert(image_path, timestamp):
    """Send email with captured image attached"""
    try:
        print("📧 Sending email alert...")

        # Create email
        msg = MIMEMultipart()
        msg['From']    = GMAIL_ADDRESS
        msg['To']      = RECEIVER_EMAIL
        msg['Subject'] = f"🚨 INTRUDER ALERT — {timestamp}"

        # Email body text
        body = f"""
🚨 MOTION DETECTED!

📅 Time  : {timestamp}
📍 Camera: Home CCTV
⚠️  Action: Check your home immediately!

This is an automated alert from your Raspberry Pi CCTV system.
        """
        msg.attach(MIMEText(body, 'plain'))

        # Attach the captured image
        with open(image_path, 'rb') as f:
            img = MIMEImage(f.read(), name="alert.jpg")
            msg.attach(img)

        # Send via Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_ADDRESS, APP_PASSWORD)
            smtp.send_message(msg)

        print("✅ Email sent successfully!")
        os.remove(image_path)

    except Exception as e:
        print(f"❌ Email failed: {e}")

def send_simple_message(subject, body):
    """Send plain text email"""
    try:
        msg = MIMEMultipart()
        msg['From']    = GMAIL_ADDRESS
        msg['To']      = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_ADDRESS, APP_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print(f"❌ Message failed: {e}")

# --- Start Camera ---
print("📷 Starting camera...")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
time.sleep(2)

print("✅ Camera ready!")
print("🔴 CCTV is LIVE — watching for motion...")

# Send startup email
send_simple_message(
    "✅ CCTV System Online",
    "Your Raspberry Pi CCTV is now ON and watching your home!"
)

# Read first two frames
ret, frame1 = cap.read()
ret, frame2 = cap.read()

last_alert_time = 0

while True:
    try:
        # Compare frames for motion
        diff   = cv2.absdiff(frame1, frame2)
        gray   = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur   = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated   = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        motion = False
        for contour in contours:
            if cv2.contourArea(contour) > SENSITIVITY:
                motion = True
                break

        current_time = time.time()
        if motion and (current_time - last_alert_time > COOLDOWN):
            now      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filename = f"/home/pi/alert_{datetime.now().strftime('%H%M%S')}.jpg"

            print(f"🚨 Motion detected at {now}!")

            # Save image
            cv2.imwrite(filename, frame1)

            # Send email with photo
            send_email_alert(filename, now)

            last_alert_time = current_time

            # Keep only last 5 alert images
            os.system("ls -t /home/pi/alert_*.jpg | tail -n +6 | xargs rm -f 2>/dev/null")

        # Move to next frame
        frame1 = frame2
        ret, frame2 = cap.read()
        time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n🛑 CCTV Stopped!")
        send_simple_message(
            "🔴 CCTV System Offline",
            "Your Raspberry Pi CCTV has been turned OFF!"
        )
        break

cap.release()
