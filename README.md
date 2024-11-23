# iRobot Create 3 - Comprehensive Robot Control and Navigation Project

This repository showcases a comprehensive project utilizing the iRobot Create 3 platform, demonstrating a wide range of robotics concepts and applications. The project is structured into multiple labs, each building upon the previous ones to create a cumulative learning experience in robot control, sensor integration, and autonomous navigation.

## Project Structure

The project is divided into three main sections, each representing a lab with increasing complexity:

### Lab 01: Basic Interactive Control Systems

This initial lab introduces fundamental concepts of robot control and sensor integration:

- **Movement & Light Control System**: Implements interactive robot control using bumper and button inputs, with dynamic speed adjustment and synchronized light patterns.
- **Proximity Detection System**: Utilizes IR sensors for real-time object detection, displaying different light colors based on object position.
- **Security Access System (CodeBreaker)**: A physical password system using the robot's interface, featuring musical and visual feedback.

### Lab 02: Advanced Control Systems

Building upon the basics, this lab introduces more complex control systems:

- **Collision Warning System**: An intelligent proximity detection system that adjusts robot speed and provides visual and audio warnings based on obstacle proximity.
- **Robot Pong**: A physical implementation of the classic Pong game, demonstrating complex motion control and sensor usage.
- **Autonomous Area Sweeper**: An intelligent room-mapping and sweeping system that explores and covers rectangular spaces efficiently.

### Lab 03: Autonomous Navigation

The final lab focuses on advanced autonomous navigation capabilities:

- **Autonomous Delivery**: Navigates towards a specified destination while avoiding obstacles, using real-time path adjustment and obstacle circumnavigation.
- **Maze Solver**: Explores and navigates through an unknown maze environment, implementing wall-following and flood-fill algorithms for efficient pathfinding.

## Key Features

- Asynchronous event handling for responsive control
- Real-time sensor data processing (IR, bumpers, buttons)
- Dynamic speed adjustment and motion control
- Visual feedback through LED patterns and colors
- Audio feedback and musical note generation
- Fail-safe mechanisms and emergency stops
- Complex geometry calculations for navigation
- Autonomous exploration and mapping
- Pathfinding and obstacle avoidance algorithms

## Technical Implementation

- Written in Python
- Utilizes asynchronous programming for real-time robot control
- Implements various mathematical calculations for spatial reasoning and decision-making
- Integrates multiple sensors for comprehensive environmental awareness
- Features custom algorithms for light patterns, navigation, and pathfinding

## Usage

1. Power on the iRobot Create 3
2. Navigate to the desired lab directory
3. Run the specific Python script for the system you want to test
4. Interact with the robot using its physical interfaces or observe its autonomous behavior

## Conclusion

This project demonstrates a wide range of robotics concepts, from basic control systems to advanced autonomous navigation. By progressing through the labs, users can gain a comprehensive understanding of robotics programming, sensor integration, and autonomous decision-making algorithms.

## Acknowledgments

Developed as part of CS 1301 - Intro to Computing, Fall 2024
