# iRobot Create 3 - Interactive Robot Control System

## Overview
This project implements three interactive control systems for the iRobot Create 3 platform, demonstrating sensor integration, event handling, and user interaction. The implementation includes a movement control system, proximity-based lighting, and a security access system.

## Features

### Movement & Light Control System
- Interactive robot control through bumper and button inputs
- Dynamic speed adjustment with auditory feedback
- Synchronized light ring patterns with movement
- Automatic speed regulation system

### Proximity Detection System
- Real-time object detection using IR sensor array
- Dynamic light ring color changes based on object position
  - Red: Object closest to left side
  - Green: Object closest to right side
  - White: Object in center or no detection
- Accurate within 2 feet range using white surfaces

### Security Access System (CodeBreaker)
A physical password system utilizing the robot's interface:
- Four-input combination system using buttons and bumpers
- Musical feedback for each input (C5-F5 notes)
- Visual feedback through LED patterns
- Celebratory light and sound display on successful access
- Auto-reset on failed attempts

## Technical Implementation
- Written in Python
- Uses asynchronous event handling for responsive control
- Implements IR sensor data processing
- Features custom light pattern algorithms
- Includes musical note generation system

## Usage
1. Power on the iRobot Create 3
2. Run the desired system:
   - `bumpers_and_buttons.py` for movement control
   - `ir_sensors.py` for proximity detection
   - `CodeBreaker.py` for security system
3. Interact with the robot using its physical interfaces

## Demo
The system includes a unique "success dance" when the correct security code is entered, featuring:
- Choreographed movement patterns
- Dynamic light displays
- Musical accompaniment

## Acknowledgments
Developed as part of CS 1301 - Intro to Computing, Fall 2024
