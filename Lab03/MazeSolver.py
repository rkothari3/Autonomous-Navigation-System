from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
from collections import deque

# robot is the instance of the robot that will allow us to call its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("BAYMAX"))  # Will connect to the first robot found.

# === FLAG VARIABLES
HAS_COLLIDED = False
HAS_ARRIVED = False
PRESS = False

# === MAZE DICTIONARY
N_X_CELLS = 3 # Size of maze (x dimension)
N_Y_CELLS = 3 # Size of maze (y dimension)
CELL_DIM = 50


# === DEFINING ORIGIN AND DESTINATION
PREV_CELL = None
START = (0,0)
CURR_CELL = START
DESTINATION = (0, 2)
# MAZE_DICT[CURR_CELL]["visited"] = True


# === PROXIMITY TOLERANCES
WALL_THRESHOLD = 80

# ==========================================================
# FAIL SAFE MECHANISMS
# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_touched(robot):
    global PRESS
    await robot.set_lights_rgb(255, 0, 0)
    await robot.set_wheel_speeds(0, 0)
    quit
    PRESS = True

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global PRESS, HAS_COLLIDED
    await robot.set_lights_rgb(255, 0, 0)
    await robot.set_wheel_speeds(0, 0)
    PRESS = True
    HAS_COLLIDED = True

# ==========================================================
# Helper Functions

def createMazeDict(nXCells, nYCells, cellDim):
    
    mazeDict = {}

    for i in range(nXCells): # Iterate through x coordinates
        for j in range(nYCells): # Iterate through y coordinates
            actual_position = (i*cellDim, j*cellDim) # Calculate the actual position of the cell

            mazeDict[(i,j)] = {
                "position": actual_position,
                "neighbors": [],
                "visited": False,
                "cost": 0
            }
    return mazeDict
# print(createMazeDict(2, 2, 10))

def addAllNeighbors(mazeDict, nXCells, nYCells):
    # directions:
    # (0,1) -> front
    # (1,0) -> right
    # (0,-1) -> back
    # (-1,0) -> left

    directions = [(-1,0), (0,1), (1,0), (0,-1)]
    
    # Iterate through each cell in the maze
    for i in range(nXCells):
        for j in range(nYCells):
                                                        # List to store valid neighbors
            neighbors = []
            
                                                        # Check each possible direction
            for dir_x, dir_y in directions:
                neighbor_x = i + dir_x
                neighbor_y = j + dir_y
                                                 # nXCells and nYCells are the dimensions of the maze
                                                                                # Same logic for neighbor_y
                                                                                # Check if the neighbor's x and y coordinates are within the maze
                if neighbor_x >= 0 and neighbor_x < nXCells:
                    if neighbor_y >= 0 and neighbor_y < nYCells:
                        if (neighbor_x, neighbor_y) in mazeDict:
                            neighbors.append((neighbor_x, neighbor_y))
            
            mazeDict[(i,j)]["neighbors"] = neighbors
    return mazeDict
# mazeDict = createMazeDict(4, 4, 20)
# print(addAllNeighbors(mazeDict, 4, 4))
# # {(0, 0): {'position': (0, 0), 'neighbors': [(0,1),(1,0)],
# # 'visited': False, 'cost': 0},
# # (0, 1): {'position': (0, 10), 'neighbors': [(1,1),(0,0)],
# # 'visited': False, 'cost': 0},
# # (1, 0): {'position': (10, 0), 'neighbors': [(1,1),(0,0)],
# # 'visited': False, 'cost': 0},
# # (1, 1): {'position': (10, 10), 'neighbors': [(0,1),(1,0)],
# # 'visited': False, 'cost': 0}}

def getRobotOrientation(heading):
    # Range of deg. for the heading
    # East: 315-360 or 0-45 degrees -> 0 or 360 degrees
    # North: 45-135 degrees -> 90 degrees
    # West: 135-225 degrees -> 180 degrees
    # South: 225-315 degrees -> 270 degrees
    
    if (heading >= 315) or (heading < 45):
        return "E"
    elif (heading >= 45) and (heading < 135):
        return "N"
    elif (heading >= 135) and (heading < 225):
        return "W"
    else:                                                                   # heading >= 225 and heading < 315
        return "S"
# print(getRobotOrientation(361))  # E
# print(getRobotOrientation(88.5))  # N

def getPotentialNeighbors(currentCell, orientation):
                                                                                        # Direction vectors for each orientation
                                                                                        # If the robot is facing E, the left vector is (0,1), front vector is (1,0), right vector is (0,-1), and back vector is (-1,0)
                                                                                        # But,if the robot is facing N, the left vector is (-1,0), front vector is (0,1), right vector is (1,0), and back vector is (0,-1)
                                                                                        # Same logic for West and South, but the vectors gonna be different.
    orientation_vectors = {
        "E": {"left": (0,1), "front": (1,0), "right": (0,-1), "back": (-1,0)},        
        "N": {"left": (-1,0), "front": (0,1), "right": (1,0), "back": (0,-1)},
        "W": {"left": (0,-1), "front": (-1,0), "right": (0,1), "back": (1,0)},
        "S": {"left": (1,0), "front": (0,-1), "right": (-1,0), "back": (0,1)}
    }
    
    vectors = orientation_vectors[orientation] # key -> orientation, value -> dictionary of vectors
    i, j = currentCell
    
                                                                                # Calculate potential neighbors [left, front, right, back] - in that specific order btw
    potentialNeighbors = [
        (i + vectors["left"][0], j + vectors["left"][1]),
        (i + vectors["front"][0], j + vectors["front"][1]),
        (i + vectors["right"][0], j + vectors["right"][1]),
        (i + vectors["back"][0], j + vectors["back"][1])
    ]
    
    return potentialNeighbors

def isValidCell(cellIndices, nXCells, nYCells): 
    x, y = cellIndices
    isValid = False
    if 0 <= x < nXCells:
        if 0 <= y < nYCells:
            isValid = True
        else:
            isValid = False
    return isValid
# print(isValidCell((3,3), 4, 5))
# # True
# print(isValidCell((1,2), 2, 2))
# # False
# print(isValidCell((-1, 0), 2, 2))
# # False

def getWallConfiguration(IR0, IR3, IR6, threshold):
    wallList = [1,2,3]
    
    # Calculate proximity readings for each IR sensor
    ir_reading0 = 4095 / (IR0 + 1)
    ir_reading3 = 4095 / (IR3 + 1)
    ir_reading6 = 4095 / (IR6 + 1)


    
    # Check if IR0 reading indicates a wall
    if ir_reading0 <= threshold:
       
        wallList[0] = True  # Wall present
    else:
        
        wallList[0] = False  # No wall
    
    # Check if IR3 reading indicates a wall
    if ir_reading3 <= threshold:
        
        wallList[1]= True  # Wall present
    else:
        
        wallList[1] = False  # No wall
    
    # Check if IR6 reading indicates a wall
    if ir_reading6 <= threshold:
    
        wallList[2] = True  # Wall present
    else:
        
        wallList[2] = False # No wall
    
    # Return the list indicating wall presence for each sensor

    return wallList

def getNavigableNeighbors(wallsAroundCell, potentialNeighbors, prevCell, nXCells, nYCells): 
# wallAroundCell (list of bools), potentialNeighbors (list of tuples), prevCell (tuple or none), nXCells (int), nYCells (int)
    navNeighbors = []
                                                                            # Check each direction (left, front, right) and corresponding potential neighbor
                                                                            # But first we got to add the prevCell b/c it definitely don't have a wall
    if prevCell != None:
        if isValidCell(prevCell, nXCells, nYCells):
            navNeighbors.append(prevCell)
    for i, hasWall in enumerate(wallsAroundCell):
        if i < len(potentialNeighbors):
            neighbor = potentialNeighbors[i]
                                                                    # Add neighbor if: no wall & within bounds.
            if hasWall == False:
                if isValidCell(neighbor, nXCells, nYCells):
                    navNeighbors.append(neighbor)
                
    return navNeighbors
# print(getNavigableNeighbors([True,True,False],[(1,2),(2,1),(1,0),(0,1)], (0,1), 2, 2))
# print(getNavigableNeighbors([False,True,False], [(0,2),(1,3),(2,2),(1,1)], (1,1), 4, 4))


def updateMazeNeighbors(mazeDict, currCell, navNeighbors):
                                                            # Iterate through each cell in the maze dictionary
    for cell, info in mazeDict.items():
                                                        # Check if the current cell is a neighbor of the cell
        if currCell in info["neighbors"]:
                                                                # If the cell is not in the navigable neighbors, remove the current cell from its neighbors
            if cell not in navNeighbors:
                mazeDict[cell]["neighbors"].remove(currCell)
                                                                # Update the neighbors of the current cell to the navigable neighbors
    mazeDict[currCell]["neighbors"] = navNeighbors

    return mazeDict

def getNextCell(mazeDict, currentCell):
                                                                        # Get the neighbors of the current cell
    neighbors = mazeDict[currentCell]["neighbors"]
    
    visited_neighbors = []
    unvisited_neighbors = []
   
                                                        # Iterate through each neighbor
    for neighbor in neighbors:
                                       
        if not mazeDict[neighbor]["visited"]:
            cost = mazeDict[neighbor]["cost"]                             
            unvisited_neighbors.append((cost, neighbor))

        else:
            cost = mazeDict[neighbor]["cost"]                                           
            visited_neighbors.append((cost, neighbor))
   
                                                        # If there are no unvisited neighbors, return None
    if len(unvisited_neighbors) == 0:
        if not len(visited_neighbors) == 0:
            visited_neighbors.sort()
            
            return visited_neighbors[0][1]
        else:
            
            return None
    else:
        unvisited_neighbors.sort()                                               # Return the neighbor with the lowest cost (last in the sorted list)
        return unvisited_neighbors[0][1]
        
    
def checkCellArrived(currentTuple, destinationTuple):
    return currentTuple == destinationTuple


def updateMazeCost(mazeDict, start, goal):
    for (i,j) in mazeDict.keys():
        mazeDict[(i,j)]["flooded"] = False

    queue = deque([goal])
    mazeDict[goal]['cost'] = 0
    mazeDict[goal]['flooded'] = True

    while queue:
        current = queue.popleft()
        current_cost = mazeDict[current]['cost']

        for neighbor in mazeDict[current]['neighbors']:
            if not mazeDict[neighbor]['flooded']:
                mazeDict[neighbor]['flooded'] = True
                mazeDict[neighbor]['cost'] = current_cost + 1
                queue.append(neighbor)

    return mazeDict


# === BUILD MAZE DICTIONARY

MAZE_DICT = createMazeDict(N_X_CELLS, N_Y_CELLS, CELL_DIM)
MAZE_DICT = addAllNeighbors(MAZE_DICT, N_X_CELLS, N_Y_CELLS)

# ==========================================================
# EXPLORATION AND NAVIGATION

# === EXPLORE MAZE
async def navigateToNextCell(robot, nextCell, orientation):
    global MAZE_DICT, PREV_CELL, CURR_CELL, CELL_DIM

    if PRESS:
            await robot.set_wheel_speeds(0,0)
            HAS_COLLIDED = True
    
    orientation_offsets = {
        "N": {"front": (0, 1), "back": (0, -1), "left": (-1, 0), "right": (1, 0)},
        "S": {"front": (0, -1), "back": (0, 1), "left": (1, 0), "right": (-1, 0)},
        "E": {"front": (1, 0), "back": (-1, 0), "left": (0, 1), "right": (0, -1)},
        "W": {"front": (-1, 0), "back": (1, 0), "left": (0, -1), "right": (0, 1)},
    }
    

    xDistance =  nextCell[0] - CURR_CELL[0]
    yDistance = nextCell[1] - CURR_CELL[1]

    directionInfo = orientation_offsets[orientation]
    newDirection = ""
    for direction, offsets in directionInfo.items():
        if (xDistance, yDistance) == offsets:
            newDirection = direction
    
    if newDirection == "back":
        await robot.turn_right(180)
    elif newDirection == "left":
        await robot.turn_left(90)
    elif newDirection == "right":
        await robot.turn_right(90)
        
    await robot.move(CELL_DIM)

    
    MAZE_DICT[CURR_CELL]["visited"] = True
    PREV_CELL = CURR_CELL
    CURR_CELL = nextCell
    

     
@event(robot.when_play)
async def navigateMaze(robot):
    global HAS_COLLIDED, HAS_ARRIVED
    global PREV_CELL, CURR_CELL, START, DESTINATION
    global MAZE_DICT, N_X_CELLS, N_Y_CELLS, CELL_DIM, WALL_THRESHOLD

    while not HAS_COLLIDED and not HAS_ARRIVED:

        if PRESS:
            await robot.set_wheel_speeds(0,0)
            HAS_COLLIDED = True
            break
        
        position = await robot.get_position()
        x = position.x
        y = position.y
        heading = position.heading

        
        
        orientation = getRobotOrientation(heading)
        potentialNeighbors = getPotentialNeighbors(CURR_CELL, orientation)

        readings = (await robot.get_ir_proximity()).sensors
        IR0 = readings[0]
        IR3 = readings[3]
        IR6 = readings[6]
        
        boolWall = getWallConfiguration(IR0, IR3, IR6, WALL_THRESHOLD)
        navNeighbors= getNavigableNeighbors(boolWall, potentialNeighbors, PREV_CELL, N_X_CELLS, N_Y_CELLS)

        MAZE_DICT = updateMazeNeighbors(MAZE_DICT, CURR_CELL, navNeighbors)
      
        MAZE_DICT = updateMazeCost(MAZE_DICT, START, DESTINATION)
       
        nextCell = getNextCell(MAZE_DICT, CURR_CELL)
    

        await navigateToNextCell(robot, nextCell, orientation)

        
        if not HAS_ARRIVED:
            if checkCellArrived(CURR_CELL, DESTINATION):
                await robot.set_lights_spin_rgb(0, 255, 0)
                HAS_ARRIVED = True
                
                
                

robot.play()
