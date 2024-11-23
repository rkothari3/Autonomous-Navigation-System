from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth("KEARSE-BOT"))   # Put robot name here.

# IR Sensor Angles
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]

# Major scale notes (C major)
MAJOR_SCALE = [Note.C4, Note.D4, Note.E4, Note.F4, Note.G4, Note.A4, Note.B4, Note.C5]
current_note_index = 0

# --------------------------------------------------------
# Implement the first two functions so that the robot
# will stop and turn on a solid red light
# when any button or bumper is pressed.
# --------------------------------------------------------
# Global Variable
press = False
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

# --------------------------------------------------------
# Implement robotPong() so that the robot:
#     Sets the initial light to cyan.
#     Moves in a straight line at 15 units/s.
#     CONTINUOUSLY checks IR readings for nearby walls.
#     If the closest wall is <= 20 units away,
#         Momentarily stop.
#         Reflect its direction based on the angle of the wall.
#         Change the light from cyan to magenta, or vice versa.
# --------------------------------------------------------

@event(robot.when_play)
async def robotPong(robot):
    """
    Use the following two lines somewhere in your code to calculate the
    angle and direction of reflection from a list of IR readings:
        (approx_dist, approx_angle) = angleOfClosestWall(ir_readings)
        (direction, turningAngle) = calculateReflectionAngle(approx_angle)
    Then, if the closest wall is less than 20 cm away, use the
    direction and the turningAngle to determine how to rotate the robot to
    reflect.
    """
    global current_note_index, press
    await robot.set_lights_rgb(0, 255, 255)
    await robot.set_wheel_speeds(15, 15)
    current_color = "cyan"
    
    while True:
        if press:
            await robot.set_wheel_speeds(0,0)
            break
        ir_readings = (await robot.get_ir_proximity()).sensors
        (approx_dist, approx_angle) = angleOfClosestWall(ir_readings)

        if approx_dist <= 20:
            await robot.set_wheel_speeds(0, 0)
            (direction, turningAngle) = calculateReflectionAngle(approx_angle)
            # Command the robot to rotate clockwise (right) or counter-clockwise (left) for a specified number of degrees.
            if direction == "right":
                await robot.turn_right(turningAngle)
            else:
                await robot.turn_left(turningAngle)
            
            # Change the light from cyan to magenta, or vice versa.
            if current_color == "cyan":
                await robot.set_lights_rgb(255, 0, 255)
                current_color = "magenta"
            else:
                await robot.set_lights_rgb(0, 255, 255)
                current_color = "cyan"
            
            await robot.play_note(MAJOR_SCALE[current_note_index], 0.5)
            current_note_index = (current_note_index + 1) % len(MAJOR_SCALE)
        
            
# current_note_index + 1 increments the index to point to the next note in the scale.
# % len(MAJOR_SCALE) ensures that the index wraps around to 0 after reaching the end of the scale.
# Modulo operation makes the index loop back to the beginning of the list, creating a continuous cycle through the notes.
            
            await robot.set_wheel_speeds(15, 15)
    
    
    

def angleOfClosestWall(readings):
    """Remember that this function can be autograded!"""
    IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
    # Initialize the closes distance and angle.
    approx_dist = float('inf')
    approx_angle = None
    # for loop thru the readings and its corresponding angles.
    for i, reading in enumerate(readings):  
        # Calculate the proximity of the wall.
        proximity = 4095 / (reading + 1)
        # Check if the proximity is less than the closest distance.
        if proximity < approx_dist:
            approx_dist = proximity
            approx_angle = IR_ANGLES[i]
    # Round the closest distance to three decimal places
    approx_dist = round(approx_dist, 3)
    # Return the closest distance and corresponding angle as a tuple
    return (approx_dist, approx_angle)

def calculateReflectionAngle(angle):
    """Remember that this function can be autograded!"""
    if angle < 0:
        direction = "right"
        turningAngle = 180 + 2 * angle
    else:
        direction = "left"
        turningAngle = 180 - 2 * angle
    
    turningAngle = round(turningAngle, 3)

    return (direction, turningAngle)

# start the robot
robot.play()
