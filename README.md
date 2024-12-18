# Hexapod Caterpie

This repository contains the **Hexapod Caterpie** project, developed as part of the subject *Artificial Intelligence Applied to Robots* in the Computer Engineering Degree at the University of Huelva. The main objective of the project was to design, implement, and configure a hexapod robot capable of detecting and recognizing nanobugs in real-time.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Project Features](#project-features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Architecture](#project-architecture)
7. [Challenges and Solutions](#challenges-and-solutions)
8. [Future Work](#future-work)
9. [Authors](#authors)
10. [License](#license)

---

## Introduction

This project involves the implementation of a hexapod robot based on the **[FreeNove Big Hexapod](https://github.com/Freenove/Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi)** model. The robot uses a YOLOv5 neural network to detect specific objects such as nanobugs of different colors and other hexapods. Additionally, it integrates a communication system between robots to coordinate actions.

The primary goal was to develop the following capabilities:

- Autonomous movement avoiding surface edges.
- Real-time detection and capture of nanobugs.
- Communication between robots to coordinate and avoid conflicts in capturing nanobugs.

---

## Project Features

1. **Autonomous Movement**: Implementation of algorithms for the robot to move while avoiding edges using distance sensors.
2. **Nanobug Detection**: Utilization of the YOLOv5 model to identify nanobugs and other hexapods.
3. **Inter-Robot Communication**: Centralized system using a server to coordinate nanobug capture and avoid interference.
4. **Decision Algorithms**: Logic based on edge detection, nanobug detection, and hexapod detection to make real-time decisions.

---

## Requirements

- **Hardware**:
  - FreeNove Big Hexapod Robot Kit.
  - Raspberry Pi (recommended model: 3B+ or higher).
  - Compatible servomotors.
  - Distance sensor (sonar).

- **Software**:
  - Python 3.8 or higher.
  - Libraries:
    - PyTorch
    - OpenCV
    - Pyro4
    - RoboFlow (for dataset management)
  - YOLOv5 (official Ultralytics implementation).

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/GrunCrow/Hexapod_Caterpie.git
   cd Hexapod_Caterpie
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the environment on the Raspberry Pi and ensure the servomotors are correctly connected.

4. Download the trained YOLOv5 model into the `models/` folder.

---

## Usage

### Basic Execution

1. Run the main script to start the robot:
   ```bash
   python main.py
   ```

2. Set up communication between robots if necessary:
   ```bash
   python server.py
   ```

### Function Details

- **Movement**: The robot moves forward, detects edges, and turns accordingly to avoid falls.
- **Object Detection**: Captures real-time images and uses YOLOv5 to identify nanobugs.
- **Coordination**: Implements a centralized protocol to avoid conflicts in nanobug capture.

---

## Project Architecture

1. **Movement Control**: Base code for calibration, turns, and robot displacement.
2. **Edge Detection**:
   - Use of sonar to measure distances and avoid falls.
   - Logic to recalibrate movement after detection.
3. **Nanobug Recognition**:
   - YOLOv5 model trained with labeled images of nanobugs and hexapods.
   - Real-time image processing from the robot's camera.
4. **Inter-Robot Communication**:
   - Client-server system based on Pyro4.

---

## Challenges and Solutions

- **Robot Assembly**: Error in the placement of the battery compartment, resolved by adjusting the assembly.
- **Servo Overheating**: Limiting the head's rotation angle to avoid collisions and damage.
- **Damaged Leg Servo**: Replacement of the defective component.

---

## Future Work

1. **Actions on Detecting Other Hexapods**: Implement additional behaviors such as reversing and turning.
2. **Improved Training**: Increase dataset quality to avoid confusion between hexapods and the background.
3. **Edge Detection Optimization**: Use depth estimation models to improve accuracy.
4. **Additional Sensors**: Incorporate more precise sensors like laser sensors.

---

## Authors

- Juan Diego Díaz
- Alberto Fernández Merchán
- Alba Márquez Rodríguez

---

## License

This project is open source under the [MIT License](LICENSE), unless otherwise stated. For more details, see the LICENSE file.

---

## References

1. [YOLOv5 by Ultralytics](https://github.com/ultralytics/yolov5)
2. [FreeNove Big Hexapod Robot Kit](https://www.freenove.com/)
3. [RoboFlow](https://app.roboflow.com/)
