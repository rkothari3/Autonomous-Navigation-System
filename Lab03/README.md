# Autonomous Robot Navigation Project

## Overview

This project implements an autonomous robot navigation system capable of handling two distinct scenarios: autonomous delivery in a room with obstacles and maze-solving. The system is designed to showcase advanced robotics concepts, including sensor-based navigation, obstacle avoidance, and pathfinding algorithms.

## Key Features

1. **Autonomous Delivery**
   - Navigates towards a specified destination while avoiding obstacles
   - Implements event-driven fail-safe mechanisms for collision prevention
   - Utilizes IR sensors for obstacle detection and proximity measurement
   - Employs real-time path adjustment and obstacle circumnavigation

2. **Maze Solver**
   - Explores and navigates through an unknown maze environment
   - Implements wall-following and flood-fill algorithms for efficient pathfinding
   - Dynamically updates maze representation as it explores
   - Provides visual feedback upon reaching the maze exit

## Technical Details

### Autonomous Delivery

- **Helper Functions**: 
  - `getMinProxApproachAngle()`: Determines closest object and its angle
  - `getCorrectionAngle()`: Calculates angle for vertical alignment
  - `getAngleToDestination()`: Computes angle to face the destination
  - `checkPositionArrived()`: Verifies if destination is reached

- **Navigation Functions**:
  - `realignRobot()`: Adjusts robot orientation towards destination
  - `moveTowardGoal()`: Directs robot towards target, avoiding obstacles
  - `followObstacle()`: Navigates around detected obstacles

- **Main Function**: `makeDelivery()`: Orchestrates the entire delivery process

### Maze Solver

- **Helper Functions**:
  - `createMazeDict()`: Initializes maze representation
  - `addAllNeighbors()`: Populates neighbor information for each cell
  - `getRobotOrientation()`: Converts heading to cardinal direction
  - `getWallConfiguration()`: Detects walls using IR sensors
  - `getNavigableNeighbors()`: Determines accessible neighboring cells
  - `updateMazeNeighbors()`: Updates maze layout based on navigation
  - `getNextCell()`: Decides the next best move

- **Navigation Functions**:
  - `navigateToNextCell()`: Moves robot to the next cell in the maze
  - `navigateMaze()`: Main function for maze navigation

## Implementation

The project is implemented in Python, utilizing asynchronous programming for real-time robot control. It incorporates various mathematical calculations for spatial reasoning and decision-making.

## Conclusion

This project demonstrates advanced capabilities in autonomous robot navigation, combining sensor data processing, real-time decision making, and efficient pathfinding algorithms. It showcases the potential of robotics in solving complex navigational challenges in both structured and unstructured environments.

[1][2]

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/38259056/6ad9532d-ac30-4ca8-b4ef-a34279a809e2/paste.txt
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/38259056/508b6502-0fb6-4738-97fb-e572d24831a7/paste-2.txt
