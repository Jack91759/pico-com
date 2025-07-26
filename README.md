# Pico Com

**Pico Com** is a serial communication terminal project using a Raspberry Pi Pico, an LCD1602 display, a relay, a buzzer, and digital I/O pins to simulate a basic interactive communication system between devices using a text-based protocol. It includes UI feedback via the LCD and buzzer, programmable commands, and page rendering over serial.

![PicoCom Setup 1](/Pictures/IMG_3238%20-%20Copy.HEIC)
![PicoCom Setup 2](/Pictures/IMG_3239%20-%20Copy.HEIC)
![PicoCom Demo](/Pictures/IMG_3241%20-%20Copy.MOV)

---

## ✨ Features

- Boot splash on LCD
- Custom device name and ID prompt
- Text message sending and receiving over GPIO pins
- LCD feedback for sent/received messages
- Basic terminal command parsing
- Relay toggle and reset signal handling
- Random ping response timing
- Buzzer alert for received messages

---

## 🧠 How It Works

This project sends and receives character data by encoding them to binary and toggling GPIO pins as digital serial lines. An underscore `_` marks characters and `~` indicates end-of-message. A custom set of page routes can be triggered remotely.

Messages are displayed on an LCD1602 (via I2C or direct GPIO), and commands like `!open /home` trigger special UI rendering back to the sender. There’s also a `!ping` responder with a randomized delay and audible buzzer feedback for underscores.

---

## 🔌 Hardware Setup

| Component        | GPIO Pin | Purpose              |
|------------------|----------|----------------------|
| TX               | GP1      | Serial Transmit Line |
| RX               | GP0      | Serial Receive Line  |
| Relay            | GP15     | Transmission Relay   |
| Buzzer (PWM)     | GP13     | Beep on special char |
| LCD1602          | I2C/SDA/SCL | Display Device ID, messages |

Ensure proper pull-ups and protection for digital IOs to avoid frying the Pico when connecting multiple devices.

---

## 📦 File Overview

- `main.py`: The complete source code for Pico Com logic
- `LCD1602.py`: LCD driver module (should be in the same folder)
- Images/Videos:
  - `IMG_3238 - Copy.HEIC`: Hardware setup (side view)
  - `IMG_3239 - Copy.HEIC`: Hardware setup (front view)
  - `IMG_3241 - Copy.MOV`: Communication demo video

---

## 🚀 Usage

1. Flash the code to your Raspberry Pi Pico (e.g., using Thonny or ampy)
2. Open serial terminal on your PC
3. Follow the LCD prompts and type your name
4. Use terminal to send messages to other connected Pico Com units
5. Try commands like:
   - `!open /home`
   - `!open /settings`
   - `!open /about`
   - `!ping`

---
## 📄 License

MIT License - free to use, modify, and distribute.

---

## 📣 Credits

Created by **Jacob**. Inspired by dialup and modern tech.

---

> Tip: If your LCD shows garbled text, double-check your wiring and contrast potentiometer on the LCD.
