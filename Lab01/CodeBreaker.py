from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

# robot is the instance of the robot that will allow us to call
# its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("VANSH-BOT")) # CHANGE ROBOT NAME

CORRECT_CODE = "341124"
current_passcode = ""

async def play_happy_tune(robot):
    await robot.play_note(Note.C5, 0.5)
    await robot.play_note(Note.E5, 0.5)
    await robot.play_note(Note.G5, 0.5)
    await robot.play_note(Note.C6, 0.5)

async def play_sad_tune(robot):
    await robot.play_note(Note.C5, 0.5)
    await robot.play_note(Note.B4, 0.5)
    await robot.play_note(Note.A4, 0.5)
    await robot.play_note(Note.G4, 0.5)

# LEFT BUTTON
@event(robot.when_touched, [True, False])  # User buttons: [(.), (..)]
async def when_left_button_touched(robot):
    global current_passcode
    current_passcode += "1"
    await robot.play_note(Note.C5, 1.0)
    await check_user_code(robot)
    

# RIGHT BUTTON
@event(robot.when_touched, [False, True])  # User buttons: [(.), (..)]
async def when_right_button_touched(robot):
    global current_passcode
    current_passcode += "2"
    await robot.play_note(Note.D5, 1.0)
    await check_user_code(robot)


# LEFT BUMP
@event(robot.when_bumped, [True, False])  # [left, right]
async def when_left_bumped(robot):
    global current_passcode
    current_passcode += "3"
    await robot.play_note(Note.E5, 1.0)
    await check_user_code(robot)

# RIGHT BUMP
@event(robot.when_bumped, [False, True]) # [left, right]
async def when_right_bumped(robot):
    global current_passcode
    current_passcode += "4"
    await robot.play_note(Note.F5, 1.0)
    await check_user_code(robot)

# Function to check if the inputted code is correct
async def check_user_code(robot):
    global current_passcode
    if len(current_passcode) != len(CORRECT_CODE):
        return  # User has not finished inputting the passcode

    if current_passcode == CORRECT_CODE:
        await robot.set_lights_rgb(0, 255, 0)  # Green lights for success
        await play_happy_tune(robot)  # Play success tune
        # Extra Credit: celebration dance
        await robot.turn_left(90)  # Turn left 90 degrees
        await robot.turn_right(180)  # Turn right 180 degrees
        await robot.set_lights_rgb(255, 0, 255)  # Flash purple lights
        await robot.turn_left(360)  # Turn left 360 degrees
        await robot.play_note(Note.G5, 0.5)  # Add celebratory notes
        await robot.play_note(Note.A5, 0.5)
        await robot.set_lights_rgb(0, 255, 255)  # Flash cyan lights
        await robot.turn_right(360)  # Turn right 360 degrees
        await robot.play_note(Note.B5, 0.5)
        await robot.play_note(Note.C6, 0.5)
        await robot.set_lights_rgb(255, 255, 0)  # Flash yellow lights
        await robot.turn_left(90)  # Turn left 90 degrees
        await robot.turn_right(180)  # Turn right 180 degrees
        await robot.set_lights_rgb(255, 0, 255)  # Flash purple lights
        await robot.turn_left(360)  # Turn left 360 degrees
        await robot.play_note(Note.G5, 0.5)  # Add celebratory notes
        await robot.play_note(Note.A5, 0.5)
        await robot.set_lights_rgb(0, 255, 255)  # Flash cyan lights
        await robot.turn_right(360)  # Turn right 360 degrees
        await robot.play_note(Note.B5, 0.5)
        await robot.play_note(Note.C6, 0.5)
        await robot.set_lights_rgb(255, 255, 0)  # Flash yellow lights

    else:
        current_passcode = ""  # Reset the input for a fresh attempt
        await robot.set_lights_rgb(255, 0, 0)  # Red lights for failure
        await play_sad_tune(robot)  # Play failure tune

# Function to initialize the robot for passcode input
@event(robot.when_play)
async def play(robot):
    await robot.set_lights_rgb(0, 0, 255)  # Blue lights to indicate ready state
    print("Robot is ready for passcode input.")

robot.play()
