from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
import math as m




robot = Create3(Bluetooth("KEARSE-BOT"))   # Put robot name here.




# --------------------------------------------------------
# Global Variables - feel free to add your own as necessary
# --------------------------------------------------------

# Behavorial
HAS_COLLIDED = False     # The robot has collided with a wall.
HAS_EXPLORED = False     # The robot has finished exploring the box.
HAS_SWEPT = False        # The robot has finished sweeping, and
                         # has arrived at its final destination.




# Spatial Awareness
SENSOR2CHECK = 0         # The index of the sensor that corresponds
                         # with the closest side wall,
                         # either 0 for left-most or -1 for right-most.
ROTATION_DIR = 0         # The direction the robot needs to explore.
CORNERS = []             # A list that stores all the corners as the robot explores.
DESTINATION = ()         # The point that is the farthest away from the robot.
                         # This point becomes the robot's final destination.




# Constants - Do not change.
ARRIVAL_THRESHOLD = 5    # We say that the robot has arrived at its final
                         # destination if the distance between the robot's
                         # position and the location of the final destination
                         # is less than or equal to this value.
SPEED = 10               # The speed at which the robot should normally move.
ROBOT_MOVE_DISTANCE = 15 # The distance by which the robot needs to move
                         # to the side to sweep a new column of the box.

press = False


# --------------------------------------------------------
# Implement these three helper functions so that they
# can be used later on.
# --------------------------------------------------------




# Helper Function 1
def farthestDistance(currPosition, positions):
    # Current positions is (x1, y1) and the tuples in the lists are (x2, y2) respectively.
    """Remember that this function can be autograded!"""
    maxDistance = 0
    farthestPosition = ()
    for x, y in positions:
       
        distance = m.sqrt((x - currPosition[0])**2 + (y - currPosition[1])**2)
        if distance > maxDistance:
            maxDistance = distance
            farthestPosition = (x, y)
    return farthestPosition




# Helper Function 2




def movementDirection(readings):
    global SENSOR2CHECK
    global ROTATION_DIR
    """Remember that this function can be autograded!"""
    right_sum = 0
    left_sum = 0
    for item in readings[:3]:
        left_sum += item




    for item in readings[-3:]:
        right_sum += item
   
    if left_sum > right_sum:
        SENSOR2CHECK = 0
        ROTATION_DIR = 1
        return "clockwise"
    else:
        SENSOR2CHECK = -1
        ROTATION_DIR = -1
        return "counterclockwise"




# Helper Function 3
def checkPositionArrived(current_position, destination, threshold):
    """Remember that this function can be autograded!"""
    # distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)
    distance = m.sqrt((destination[0] - current_position[0])**2 + (destination[1] - current_position[1])**2)
    # If the distance between the current position and the destination is less than or equal to the threshold, return True
    # Otherwise, return False
    if distance <= threshold:
        return True
    else:
        return False
   




# --------------------------------------------------------
# Implement the these two functions so that the robot
# will stop and turn on a solid red light
# when any button or bumper is pressed.
# --------------------------------------------------------




# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_button_touched(robot):
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



# --------------------------------------------------------








@event(robot.when_play)
async def play(robot):
    global HAS_COLLIDED, HAS_EXPLORED, HAS_SWEPT, SENSOR2CHECK
    global ROTATION_DIR, CORNERS, DESTINATION, ARRIVAL_THRESHOLD
    global SPEED, ROBOT_MOVE_DISTANCE
    global press
    #movementDirection(readings)


   
    await robot.reset_navigation()
   
   
    readings = (await robot.get_ir_proximity()).sensors
    movementDirection(readings)
    await robot.set_wheel_speeds(SPEED, SPEED)
    # HAS_EXPLORED = True
    # Main exploration and sweeping loop
    while not HAS_SWEPT:
        if press:
            await robot.set_lights_rgb(255, 0, 0)
            await robot.set_wheel_speeds(0, 0)
            break
        if not HAS_EXPLORED:
            await explore(robot)
            await robot.set_lights_rgb(180,0,147)
           
   
        else:
            await sweep(robot)
           
# --------------------------------------------------------
# Implement explore such that the robot:
#     Finds the front and side proximity to a wall.
#     If there is a wall within 10 units in front,
#         stop, turn 90 degrees, and continue.
#     When all four corners have been found, determine
#         the furthest corner from the robot with farthestDistance()
#     Auto-aligns with the side boundary if the robot drifts
#         away from the side wall.
# --------------------------------------------------------




async def explore(robot):
    global HAS_COLLIDED, HAS_EXPLORED, HAS_SWEPT, SENSOR2CHECK
    global ROTATION_DIR, CORNERS, DESTINATION, ARRIVAL_THRESHOLD
    global SPEED, ROBOT_MOVE_DISTANCE




   


    readings = (await robot.get_ir_proximity()).sensors
    #movementDirection(readings)
    front_proximity = 4095 / (readings[3] + 1)
    side_proximity = 4095 / (readings[SENSOR2CHECK] + 1)
   
   


    #ROTATION_DIR = "clockwise"
    if front_proximity < 10:
        # Record the corner position
        position = await robot.get_position()
       
       
        CORNERS.append((position.x, position.y))
       
       
        #await robot.set_wheel_speeds(SPEED, SPEED)
        if len(CORNERS) == 4:
           
            print(CORNERS)
            DESTINATION = farthestDistance((position.x, position.y), CORNERS) # def farthestDistance(currPosition, positions)
            HAS_EXPLORED = True # Setting this to True will stop the robot from exploring further
            print(f"{DESTINATION} is the farthest corner from the robot.")
       
            #await robot.set_wheel_speeds(0, 0)
           
        else:
            await robot.set_wheel_speeds(SPEED,SPEED)
            print(CORNERS)
            if ROTATION_DIR == 1:
                await robot.turn_right(90)
            else:
                await robot.turn_left(90)
    else:
        await robot.set_wheel_speeds(SPEED, SPEED)




           
   
        # Check alignment
   
    if side_proximity < 5:  # Too close to the wall
        if ROTATION_DIR == 1:
           
            await robot.turn_right(3)  # Turn away from the wall
           
        else:
           
            await robot.turn_left(3)
    elif side_proximity > 10:  # Too far from the wall
        if ROTATION_DIR == 1:


            await robot.turn_left(3)  # Turn towards the wall
           
        else:
         
            await robot.turn_right(3)
           
# --------------------------------------------------------
# Implement sweep such that the robot:
#     Checks if it has reached its final destination with
#         checkPositionArrived()
#     If the robot did reach its destination, stop, set
#         lights to green, and play a happy tune.
#     Else, if the robot's front proximity to a wall is <= 10 units,
#         stop, turn 90 degrees, move forwards by ROBOT_MOVE_DISTANCE,
#         turn 90 degrees again, and start again.
# --------------------------------------------------------




async def sweep(robot): # Change tolerance for sweep and changed the baby steps
    global HAS_COLLIDED, HAS_EXPLORED, HAS_SWEPT, SENSOR2CHECK
    global ROTATION_DIR, CORNERS, DESTINATION, ARRIVAL_THRESHOLD
    global SPEED, ROBOT_MOVE_DISTANCE


    position = await robot.get_position()

    if checkPositionArrived((position.x, position.y), DESTINATION, ARRIVAL_THRESHOLD): # if the x, y coordinate are within a certain threshold of the destination.
        await robot.set_wheel_speeds(0, 0)
        await robot.set_lights_spin_rgb(0, 255, 0)
        await robot.play_note(Note.C4, 0.5)
        HAS_SWEPT = True
        return

    readings = (await robot.get_ir_proximity()).sensors
    front_proximity = 4095 / (readings[3] + 1) # '''Is 3 in readings[3] the front sensor?'''
    if front_proximity <= 10:
        await robot.set_wheel_speeds(0, 0)
        if ROTATION_DIR == 1:
            await robot.turn_right(90)
            readings = (await robot.get_ir_proximity()).sensors
            front_proximity = 4095 / (readings[3] + 1)
            if front_proximity < ROBOT_MOVE_DISTANCE:
                await robot.move(front_proximity / 3)
            else:
                await robot.move(ROBOT_MOVE_DISTANCE)


            await robot.turn_right(90)
            await robot.set_wheel_speeds(SPEED, SPEED)
            ROTATION_DIR = -1 * ROTATION_DIR


        else:
            await robot.turn_left(90)
            readings = (await robot.get_ir_proximity()).sensors
            front_proximity = 4095 / (readings[3] + 1)
            if front_proximity < ROBOT_MOVE_DISTANCE:
                await robot.move(front_proximity / 3)
            else:
                await robot.move(ROBOT_MOVE_DISTANCE)


            await robot.turn_left(90)
           
            ROTATION_DIR = -1 * ROTATION_DIR
    else:
        await robot.set_wheel_speeds(SPEED, SPEED)


       
       
   




# start the robot
robot.play()