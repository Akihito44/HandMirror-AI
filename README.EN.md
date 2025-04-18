# HandMirror-AI 🤖🖐️

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Open Issues](https://img.shields.io/github/issues/Akihito44/HandMirror-AI)](https://github.com/Akihito44/HandMirror-AI/issues)
[![Arduino IDE](https://img.shields.io/badge/arduino_ide-2.3.6-red.svg)](https://www.arduino.cc/en/software/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/opencv-4.11.0-green.svg)](https://opencv.org/)
[![Mediapipe](https://img.shields.io/badge/mediapipe-0.10.5-red.svg)](https://mediapipe.dev/)

*Read this in other languages: [Italian](README.md).*

## 📖 Table of Contents
- [🎥 Overview](#overview)
- [🔥 Features](#features)
- [🛠️ Required Components](#required-components)
- [⚙️ Installation](#installation-and-configuration)
- [🚀 Usage](#project-execution)
- [🧠 Technical Notes](#technical-notes)
- [🔍 Troubleshooting](#troubleshooting)
- [📄 License](#license)

## Overview
HandMirror-AI is a real-time robotic hand control system powered by Artificial Intelligence. Using MediaPipe for gesture recognition and an ESP32-S3 module to drive servos, it accurately replicates your hand movements on robotic fingers.

![Demo](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGQ5Z2F0dWl0bHh4NWR1M3hqZ2Y4Y2R1dGF5dWl6dXh1dG1vZ3J2dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7kn27lnYSAxQWHo2aK/giphy.gif)

## Features
- 🎯 **Real-time hand tracking** at 30 FPS
- 🤖 **Advanced AI** with MediaPipe pipeline and optimized CNN model
- ⚙️ **Automatic calibration** of servo motors for maximum precision
- 🌐 **Cross-platform**: Windows, macOS, Linux

## Required Components
### Essential Hardware
| Component    | Qty | Specifications       |
| ------------ | :-: | ------------------- |
| ESP32-S3     | 1   | 240MHz, 512KB PSRAM |
| SG90 Servo   | 5   | 180°, 0.12s/60°     |
| Power Supply | 1   | 5V DC               |
| Jumper Wires | ~20 | M-M and M-F         |
| Webcam       | 1   | USB or built-in     |

### Optional Hardware
| Component   | Qty | Specifications |
| ----------- | :-: | -------------- |
| Breadboard  | 1   | Full size      |
| Capacitors  | 5   | 480μF, 16V     |

### Required Software
  - **Python 3.11** + libraries: `opencv-python`, `mediapipe==0.10.5`, `pyserial`
  - **Arduino IDE** (≥ v2.3.6) with **ESP32** support

## Installation and Configuration
### Repository Download
- **Via git terminal**:
   ```bash
   git clone https://github.com/Akihito44/HandMirror-AI.git
   cd HandMirror-AI
   ```
- **ZIP Download**:
  - Download from GitHub: [click here](https://github.com/Akihito44/HandMirror-AI/archive/refs/heads/main.zip)
  - Extract to destination folder

### Python Virtual Environment Setup
1. **Create virtual environment**:
   ```bash
   python -m venv myenv
   ```

2. **Activate environment**:
   - **Windows**:
     ```bash
     .\myenv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source myenv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install pyserial opencv-python mediapipe=0.10.5
   ```

### Arduino IDE Setup
1. **Update board manager**:
   - `File → Preferences → Additional Boards Manager URLs`
   - Add this URL:  
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
2. **Add ESP32 boards**:
   - `Tools → Board → Boards Manager`
   - Search for `esp32`
   - Install `Espressif Systems` package
3. **Select board**:
   - `Tools → Board → esp32`
   - Select `ESP32S3 Dev Module`
4. **Select port**:
   - `Tools → Port`
   - Select serial port (COMx on Windows or /dev/ttyUSB* on Linux)
5. **Configure board parameters**:
   - In `Tools` select board parameters
   - Example for *Freenove ESP32-S3-WROOM*:  
   ![Configuration](./images/Arduino_Configuration.png)

> ⚠️ Don't forget to install CH343 drivers if system doesn't recognize ESP32:
> - **Windows**:
>   - Download [CH343 driver](https://www.wch.cn/downloads/CH343SER_EXE.html)
>   - Filename: `CH343SER.EXE`
> - **Mac**:
>   - Download [CH343 driver](https://www.wch.cn/downloads/CH343SER_EXE.html)
>   - Filename: `CH34XSER_MAC.ZIP`
> - **Linux**:
>   - Download [CH343 driver](https://github.com/Akihito44/CH343-serial-driver/tree/main/Linux/ch343_ser_linux)
>   - Follow instructions in `README.md`

### ESP32 Configuration
1. **Connect servos** to pins defined in `Arduino-code.ino`:
   ```
   Thumb: GPIO9
   Index: GPIO10
   Middle: GPIO11
   Ring: GPIO12
   Pinky: GPIO13
   ```
   ![Circuit diagrams for ESP32 and Arduino UNO](./images/circuiti.png)
2. **Upload firmware**:
   - Open `Arduino-code.ino` in Arduino IDE
   - Select "ESP32-S3 Dev Module" board
   - Set correct serial port (e.g. `COM3` on Windows)
   - Compile and upload code

## Project Execution
### Basic Mode (Vision Only)
- **Run Python script**:
   ```bash
   python Test-HandMirror-AI.py
   ```
- **Output**: Window with landmark overlay and calculated angles

### Complete Mode (Robot Control)
1. **Configure serial port (if needed)**:
   - Modify `port='COM3'` in `HandMirror-AI.py` for your system
   - Modify `baudrate=115200` in `HandMirror-AI.py` for your board
2. **Run Python script**:
   ```bash
   python HandMirror-AI.py
   ```
3. **Usage**:
   - Show your hand to the webcam
   - Detected fingers will control servos (1 = bent, 0 = extended)
   - Press `Q` to quit

## Technical Notes
### Artificial Intelligence
1. **Recognition Pipeline**:
   ```mermaid
   graph LR
   A[Webcam Input] --> B[Landmark Detection]
   B --> C[Gesture Classification]
   C --> D[Serial Command Generation]
   D --> E[Servo Control]
   ```
2. **MediaPipe Hands**:
   - Lightweight CNN model (Convolutional Neural Network)
   - Output: 21 3D landmarks per hand
   - Accuracy >95% on internal datasets
   - Latency: ~8ms on modern CPU

### Code Architecture
| Component     | Technology        | Function                             |
| ------------ | ---------------- | ------------------------------------ |
| Vision Engine | OpenCV + MediaPipe | Hand landmark extraction             |
| Serial Bridge | PySerial         | Bidirectional ESP32 communication    |
| Control Logic | Custom Python    | Landmark to servo angle conversion   |
| Firmware     | Arduino C++      | PWM generation for servos            |

### Known Limitations
- **Total Latency**: ~120ms (webcam 60ms + processing 40ms + serial 20ms)
- **Angular Resolution**: 1° (servo hardware limit)
- **Light Conditions**: Reduced performance under <300 lux

### Project Structure
```
HandMirror-AI/
|
├── HandMirror-AI.py       # Main script for hand tracking and serial communication
├── Test-Mirror-AI.py      # Test script for hand tracking only
├── Arduino-code/
|   └── Arduino-code.ino   # Servo motor control firmware
├── images/
|   ├── Arduino_Configuration.png
|   ├── arduino.png
|   ├── circuiti.png
|   └── esp32.png
├── README.md
└── LICENSE
```

## Troubleshooting
- **Serial Port Error**:
  - Verify ESP32 is connected and recognized
  - Ensure serial drivers are installed (CH343 driver: [download here](https://github.com/Akihito44/CH343-serial-driver))
  - Close other programs using serial port (e.g., Arduino Serial Monitor)
  - Close other programs using webcam
- **Missing Dependency**:
  ```bash
  pip install --upgrade [library_name]
  ```
- **Other Issues**:
  - Check the [issues section](https://img.shields.io/github/issues/Akihito44/HandMirror-AI)

## License
Distributed under MIT License. See [LICENSE](LICENSE) for details.

*Created with ❤️ by Akihito44*
