import os
from getkey import getkey, keys
import random
import time
import threading

print("\n\n\nClick 'space' button")
# Constants
up = 'w'
down = 's'
left = 'a'
right = 'd'
spawn = ' '

# Helper function
def createList(content, times):
    List = []
    for i in range(times):
        List.append(content)
    return List

# Display functions
def clear_terminal():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
        
def textWithRandomColor(text):
    text = f"\033[{random.randint(91, 96)};1;1m{text}\033[0m"
    return text

def renderScreen(screen, resolution):
    for i in range(int(resolution['y'])):
        print(f" {''.join(screen[int(resolution['y']) - i - 1])}")

def boomAnimation(y, x, screen):
    for i in range(1, 5):
        if i == 1:
            screen[y + 1][x], screen[y - 1][x] = textWithRandomColor('|'), textWithRandomColor('|')
            screen[y][x + 1], screen[y][x - 1] = textWithRandomColor('─'), textWithRandomColor('─')
            screen[y][x] = fillSkin
        elif i == 2:
            screen[y + 1][x - 1], screen[y - 1][x + 1] = textWithRandomColor('\\'), textWithRandomColor('\\')
            screen[y - 1][x - 1], screen[y + 1][x + 1] = textWithRandomColor('/'), textWithRandomColor('/')
            screen[y][x] = pointGiverSkin
        elif i == 3:
            screen[y + 1][x], screen[y - 1][x] = fillSkin, fillSkin
            screen[y][x + 1], screen[y][x - 1] = fillSkin, fillSkin
            screen[y][x] = fillSkin
        elif i == 4:
            screen[y + 1][x - 1], screen[y - 1][x + 1] = fillSkin, fillSkin
            screen[y - 1][x - 1], screen[y + 1][x + 1] = fillSkin, fillSkin
            screen[y][x] = pointGiverSkin

        clear_terminal()
        renderScreen(screen, resolution)
        time.sleep(0.13)
# Game logic functions
def changeBlocks(changeFrom, changeTo, previousIndex, x, y):
    playableScreen[previousIndex['y']][previousIndex['x']] = changeFrom
    playableScreen[y][x] = changeTo
    previousIndex['x'] = x
    previousIndex['y'] = y

# User input handling
def handle_user_movement(user_input):
    global playerSkin, previousPlayerIndex, points

    if user_input == spawn:
        playerSkin = '\033[36;1;1m○\033[0m' #cyan
        changeBlocks(changeFrom=fillSkin, changeTo=playerSkin, previousIndex=previousPlayerIndex, x=2, y=2)
        changeBlocks(changeFrom=fillSkin, changeTo= pointGiverSkin, previousIndex=previousPointGiverIndex, x= random.randint(2, len(playableScreen[1]) - 3),y=random.randint(2, len(playableScreen) - 3))

    elif user_input == up:
        playerSkin = '\033[36;1;1m▲\033[0m' #cyan
        if previousPlayerIndex['y'] + 1 != int(resolution['y']) - 2:
            changeBlocks(changeFrom=fillSkin, changeTo=playerSkin, previousIndex=previousPlayerIndex, x=previousPlayerIndex['x'], y=previousPlayerIndex['y'] + 1)

    elif user_input == down:
        playerSkin = '\033[36;1;1m▼\033[0m' #cyan
        if previousPlayerIndex['y'] - 1 != 1:
            changeBlocks(changeFrom=fillSkin, changeTo=playerSkin, previousIndex=previousPlayerIndex, x=previousPlayerIndex['x'], y=previousPlayerIndex['y'] - 1)

    elif user_input == left:
        playerSkin = '\033[36;1;1m◄\033[0m' #cyan
        if previousPlayerIndex['x'] - 1 != 1: #change the 1 to 0 if you want the border to be 1 block thick
            changeBlocks(changeFrom=fillSkin, changeTo=playerSkin, previousIndex=previousPlayerIndex, x=previousPlayerIndex['x'] - 1, y=previousPlayerIndex['y'])

    elif user_input == right:
        playerSkin = '\033[36;1;1m►\033[0m' #cyan
        if previousPlayerIndex['x'] + 1 != int(resolution['x']) - 2:
            changeBlocks(changeFrom=fillSkin, changeTo=playerSkin, previousIndex=previousPlayerIndex, x=previousPlayerIndex['x'] + 1, y=previousPlayerIndex['y'])
            
            
    if previousPointGiverIndex['x'] == previousPlayerIndex['x'] and previousPointGiverIndex['y'] == previousPlayerIndex['y']:
        threading.Thread(target=boomAnimation(previousPointGiverIndex['y'], previousPointGiverIndex['x'], playableScreen)).start()
        points += 1
        changeBlocks(changeFrom = playerSkin, changeTo=pointGiverSkin, previousIndex=previousPointGiverIndex, x= random.randint(2, len(playableScreen[1]) - 3),y=random.randint(2, len(playableScreen) - 3))

# Main code
logs = []

resolution = {
    "y": 20,
    "x": 35
}

points = 0
isTouchingPoint = False

fillSkin = ' ' #'□'
playerSkin = "\033[36;1;1m○\033[0m" #'○'   '■' 
pointGiverSkin = "\033[92;1;4m♦\033[0m"
borderSkin = '▒'

playableScreen = [createList(fillSkin, int(resolution['x'])) for _ in range(int(resolution['y']))]

#for index, fill in enumerate(playableScreen):
#    playableScreen[index].remove(fillSkin)
#    playableScreen[index].remove(fillSkin)
#    playableScreen[index].append(borderSkin)
#    playableScreen[index].insert(0, borderSkin)
#playableScreen.append((len(playableScreen[0]) + 2) * '▒')
#playableScreen.insert(0, (len(playableScreen[0]) + 2) * '▒')


previousPlayerIndex = {
    'x': 2,
    'y': 2
}

previousPointGiverIndex = {
    'x': random.randint(2, len(playableScreen[1]) - 1),
    'y': random.randint(2, len(playableScreen) - 1)
}

while True:
    user_input = getkey()
    handle_user_movement(user_input)
    if user_input == '\x1b':
        break
     
    clear_terminal()
    renderScreen(playableScreen, resolution)

#clear_terminal()
print(f'                            Points: {str(points)}')
print(logs)