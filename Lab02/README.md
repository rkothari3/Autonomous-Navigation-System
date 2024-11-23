# iRobot Create 3 - Advanced Robot Control Systems

## Overview
This project implements three sophisticated control systems for the iRobot Create 3: a collision warning system, a robot pong game, and an autonomous area sweeper. Each system demonstrates different aspects of robotics control, sensor integration, and autonomous navigation.

## Systems

### 1. Collision Warning System
An intelligent proximity detection system that:
- Monitors front-facing IR sensors for obstacles
- Adjusts robot speed based on proximity thresholds:
  - Full stop & red light (≤ 5.0 units)
  - Slow speed & orange light (≤ 30.0 units)
  - Moderate speed & yellow light (≤ 100.0 units)
  - Full speed & green light (> 100.0 units)
- Features escalating audio warnings
- Includes fail-safe mechanisms for manual stopping

### 2. Robot Pong
A physical implementation of the classic Pong game where the robot:
- Moves in straight lines at 15 units/second
- Detects walls using IR sensors
- Calculates reflection angles for realistic bouncing
- Alternates between cyan and magenta lights on bounces
- Includes musical scale progression on wall contacts (bonus feature)
- Features emergency stop controls

### 3. Autonomous Area Sweeper
An intelligent room-mapping and sweeping system that:
- Explores and maps rectangular spaces
- Executes in two phases:
  1. Boundary exploration
  2. Systematic area coverage
- Features smart corner detection
- Implements efficient path planning
- Maintains consistent wall distance
- Includes completion detection

## Technical Implementation
- Written in Python
- Uses asynchronous event handling
- Implements complex geometry calculations
- Features fail-safe collision detection
- Uses multiple sensor integration
- Includes dynamic speed control
- Features visual and audio feedback systems

## Key Features
- Real-time sensor processing
- Dynamic speed adjustment
- Visual feedback through LED patterns
- Audio feedback system
- Fail-safe emergency stops
- Autonomous navigation
- Smart path planning

## Acknowledgments
Developed as part of CS 1301 - Intro to Computing, Fall 2024
