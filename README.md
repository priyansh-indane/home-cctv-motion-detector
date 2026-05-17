# 🔴 Raspberry Pi Zero 2W — Home CCTV with Gmail Alerts

A lightweight motion detection CCTV system built on the **Raspberry Pi Zero 2W**. Detects movement via a USB/Pi camera, captures a photo, and instantly sends a **Gmail alert with the image attached** — all running on a device the size of a stick of gum.

---

## 📸 How It Works

```
Camera detects motion → Photo captured → Gmail alert sent with photo attached
```

- Compares consecutive frames using OpenCV
- Triggers only when movement exceeds a sensitivity threshold
- Sends an email with timestamp and photo
- Cooldown timer prevents alert spam
- Auto-starts on boot via cron

---

## 🛒 Hardware Required

| Component | Details |
|-----------|---------|
| Raspberry Pi Zero 2W | Main board |
| MicroSD card | 8GB+ recommended |
| USB camera or Pi Camera Module | Any V4L2-compatible camera |
| Micro USB power supply | 5V 2A |
| USB OTG adapter | For USB cameras |

> ⚠️ The Pi Zero 2W has 512MB RAM. The script is optimised to run within these limits using 640×480 resolution.

---

## 📁 Project Structure

```
📦 pi-cctv/
├── cctv.py            # Main motion detection + alert script
├── requirements.txt   # Python dependencies
├── .gitignore         # Keeps credentials out of Git
└── README.md          # You are here
```

---

## ⚙️ Setup Guide

### Part 1 — Gmail Setup (on your phone/laptop)

**Step 1 — Enable 2-Step Verification**
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click **Security** → **2-Step Verification** → Turn it **ON**

**Step 2 — Create an App Password**
1. Go to [myaccount.google.com](https://myaccount.google.com) → **Security**
2. Search for **App Passwords** in the search bar
3. App name: `MyCCTV` → Click **Create**
4. Google gives you a **16-character password** — copy and save it

> This is NOT your regular Gmail password. It's a special password just for this app.

---

### Part 2 — Raspberry Pi Setup

**Step 3 — Install dependency**

```bash
pip3 install secure-smtplib --break-system-packages
```

**Step 4 — Clone this repo**

```bash
git clone https://github.com/YOUR_USERNAME/pi-cctv.git
cd pi-cctv
```

**Step 5 — Add your Gmail credentials**

Open `cctv.py` and edit the top section:

```python
GMAIL_ADDRESS  = "your_email@gmail.com"     # Your Gmail
APP_PASSWORD   = "abcd efgh ijkl mnop"      # App password from Step 2
RECEIVER_EMAIL = "your_email@gmail.com"     # Who gets the alert
SENSITIVITY    = 3000   # Lower = more sensitive
COOLDOWN       = 30     # Seconds between alerts
```

**Step 6 — Run it**

```bash
python3 cctv.py
```

You should see:

```
📷 Starting camera...
✅ Camera ready!
🔴 CCTV is LIVE — watching for motion...
```

And you'll receive a **"CCTV System Online"** email right away.

---

### Part 3 — Auto Start on Boot

```bash
crontab -e
```

Add this line at the bottom:

```bash
@reboot sleep 15 && python3 /home/pi/cctv.py &
```

Save: `Ctrl+X` → `Y` → `Enter`

Now the CCTV starts automatically every time the Pi powers on.

---

## 🧪 Testing

1. Wave your hand in front of the camera
2. Wait 3–4 seconds
3. Check your Gmail inbox

You'll receive an email like:

```
Subject: 🚨 INTRUDER ALERT — 2026-05-17 10:30:45

🚨 MOTION DETECTED!
🗓 Time   : 2026-05-17 10:30:45
📍 Camera : Home CCTV
⚠️  Action : Check your home immediately!
```

With the **captured photo attached**.


## 📦 Dependencies

```
secure-smtplib
opencv-python   # install via: pip3 install opencv-python --break-system-packages
```

---





