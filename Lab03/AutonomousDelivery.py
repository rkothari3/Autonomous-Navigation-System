from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import math as m

# robot is the instance of the robot that will allow us to call its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("BAYMAX"))  # Will connect to the first robot found.

HAS_COLLIDED = False
HAS_REALIGNED = False
HAS_FOUND_OBSTACLE = False
SENSOR2CHECK = 0
HAS_ARRIVED = False
DESTINATION = (0, 100)
ARRIVAL_THRESHOLD = 5
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
press = False

# Implementation for fail-safe robots
# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_touched(robot):
    global press
    await robot.set_lights_rgb(255, 0, 0)
    await robot.set_wheel_speeds(0, 0)
    press = True

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global press
    await robot.set_lights_rgb(255, 0, 0)
    await robot.set_wheel_speeds(0, 0)
    press = True

# ==========================================================

# Helper Functions
def getMinProxApproachAngle(readings):
    global IR_ANGLES
    closest_dist = float('inf')
    closest_angle = None
                                                # for loop thru the readings and its corresponding angles.
    for i, reading in enumerate(readings):  
                                                # Calculate the proximity of the wall.
        proximity = 4095 / (reading + 1)
                                                # Check if the proximity is less than the closest distance.
        if proximity < closest_dist:
            closest_dist = proximity
            closest_angle = IR_ANGLES[i]
                                                # Round the closest distance to three decimal places
    closest_distance = round(closest_dist, 3)
                                                # Return the closest distance and corresponding angle as a tuple
    return (closest_distance, closest_angle)

# print(getMinProxApproachAngle([34.2, 75.3, 732.4, 24, 63.2, 82.3, 95.6]))
# print(getMinProxApproachAngle([93.4, 41.6, 43.7, 23.6, 94.3, 52.5, 205.3]))
    
def getCorrectionAngle(heading):  
    return int(heading - 90)


def getAngleToDestination(currentPosition, destination):
    x1, y1 = currentPosition
    x2, y2 = destination
    angle = m.degrees(m.atan2(x2 - x1, y2 - y1))
    return int(angle)
# currentPosition = (1, 1)
# destination = (5, 3)
# print(getAngleToDestination(currentPosition, destination))
# currentPosition = (5, 5) 
# destination = (1, 1) 
# print(getAngleToDestination(currentPosition, destination))
# current position (x,y) in cm
# destination (x,y) in cm 

def checkPositionArrived(current_position, destination, threshold):                                 # current_position = (x, y), destination = (x, y), threshold = int
                                                                                                        # distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)
    distance = m.sqrt((destination[0] - current_position[0])**2 + (destination[1] - current_position[1])**2)
                                                                                                            # If the distance between the current position and the destination is less than or equal to the threshold, return True
    # Otherwise, return False
    if distance <= threshold:
        return True
    else:
        return False
# currentPosition = (97, 99)
# destination = (100, 100)
# threshold = 5.0
# has_arrived = checkPositionArrived(currentPosition, destination, threshold)
# print(f"Has the robot arrived at the destination? {has_arrived}")
# currentPosition = (50, 50)
# destination = (45, 55)
# threshold = 5.0
# has_arrived = checkPositionArrived(currentPosition, destination, threshold)
# print(f"Has the robot arrived at the destination? {has_arrived}")

# === REALIGNMENT BEHAVIOR
async def realignRobot(robot):
    global HAS_REALIGNED, DESTINATION
    HAS_REALIGNED = True
    position = await robot.get_position()
    x = position.x
    y = position.y
    heading = position.heading
    
    await robot.set_wheel_speeds(0, 0)
    angle = getCorrectionAngle(heading)
    await robot.turn_right(angle)
    Destination_angle = getAngleToDestination((x, y), DESTINATION)
    await robot.turn_right(Destination_angle)
    return

# === MOVE TO GOAL
async def moveTowardGoal(robot):
    global SENSOR2CHECK, HAS_FOUND_OBSTACLE, HAS_REALIGNED, IR_ANGLES

    # position = await robot.get_position()
    ir_readings = (await robot.get_ir_proximity()).sensors
    (dist, angle) = getMinProxApproachAngle(ir_readings)

    if dist > 20:
        await robot.set_wheel_speeds(5, 5)
    else:

        await robot.set_wheel_speeds(0,0)

        if angle > 0:
            await robot.turn_left(90 - angle)
            SENSOR2CHECK = 6
        else:
            await robot.turn_right(90 + angle)
            SENSOR2CHECK = 0
        HAS_FOUND_OBSTACLE = True
        

# === FOLLOW OBSTACLE

async def followObstacle(): # NOT SUPER SURE WITH THIS ONE
    global HAS_FOUND_OBSTACLE, SENSOR2CHECK, HAS_REALIGNED

    while True:
        ir_readings = (await robot.get_ir_proximity()).sensors
        proximity = 4095 / (ir_readings[SENSOR2CHECK] + 1)
        
        

        if proximity < 20.0:

            if SENSOR2CHECK == 0: # close to the wall on the right side
                await robot.turn_right(3)
    
                
            else:
                await robot.turn_left(3)
                
        await robot.set_wheel_speeds(5,5)    
        if proximity > 100.0:
            await robot.move(33)
            HAS_FOUND_OBSTACLE = False
            HAS_REALIGNED = False
            break

        

        
# ==========================================================

# Main function

@event(robot.when_play)
async def makeDelivery(robot):
    global HAS_ARRIVED, HAS_REALIGNED, HAS_COLLIDED,PRESS, DESTINATION, ARRIVAL_THRESHOLD, HAS_FOUND_OBSTACLE
    while HAS_ARRIVED == False:
        position = await robot.get_position()
        current_position = (position.x, position.y)
        HAS_ARRIVED = checkPositionArrived(current_position, DESTINATION, ARRIVAL_THRESHOLD)

        if press:
            await robot.set_wheel_speeds(0,0)
            break

        if HAS_ARRIVED == True:
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights_spin_rgb(0, 255, 0)
            break
        else:
            if HAS_REALIGNED == False:
                await realignRobot(robot)
            
            if HAS_FOUND_OBSTACLE == False:
                await moveTowardGoal(robot)
            else: 
                await followObstacle()
    
        


# start the robot
robot.play()
