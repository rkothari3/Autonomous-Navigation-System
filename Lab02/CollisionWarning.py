from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth("KEARSE-BOT"))   # Put robot name here.

# --------------------------------------------------------
# Implement the first two functions so that the robot
# will stop and turn on a solid red light
# when any button or bumper is pressed.
# --------------------------------------------------------

# Global Variables
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
# Implement avoidCollision() so that the robot CONTINUOUSLY 
# reads the IR measurement from the CENTER sensor.
# When the robot senses that the wall in front of the robot is:
#     <= 5 units away, stop the robot, set a red light, and play D7.
#     <= 30 units away, slow down the robot to 1 unit/s, set an orange light,
#        and play D6.
#     <= 100 units away, move the robot at a moderate speed (4 units/s), 
#        set a yellow light, and play D5.
#     > 100 units away, proceed at a faster pace (8 units/s), set a green light.
# --------------------------------------------------------

# CONTINUOUSLY CHECK THE IR SENSOR MEASURESMENTS FROM THE CENTER SENSOR.
@event(robot.when_play)
async def avoidCollision(robot):
    global press
    while not press:
        ir_readings = await robot.get_ir_proximity()
        center_reading = ir_readings.sensors[3] # [3] is the center sensor in the ir_readings list
        distance = 4095 / (center_reading + 1)

        if press:
            await robot.set_lights_rgb(255, 0, 0)
            await robot.set_wheel_speeds(0, 0)
            break
        
        if distance <= 5:
            await robot.set_wheel_speeds(0, 0)
            await robot.set_lights_rgb(255, 0, 0)
            await robot.play_note(Note.D7, 0.5)
            break # Are we supposed to break here?
        elif distance <= 30:
            await robot.set_wheel_speeds(1, 1)
            await robot.set_lights_rgb(255, 165, 0)
            await robot.play_note(Note.D6, 0.5)
        elif distance <= 100:
            await robot.set_wheel_speeds(4, 4)
            await robot.set_lights_rgb(255, 255, 0)
            await robot.play_note(Note.D5, 0.5)
        else:
            await robot.set_wheel_speeds(8, 8)
            await robot.set_lights_rgb(0, 255, 0)


# start the robot
robot.play()
