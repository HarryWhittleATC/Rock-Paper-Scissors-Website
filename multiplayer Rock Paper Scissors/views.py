from flask import Blueprint, render_template, request
import time
import random
views = Blueprint(__name__, "v")

global has1chosen
global has2chosen
has1chosen = False
has2chosen = False


waiting = False
gameidsinuse = []
choices1 = []
choices1ids = []
choices2 = []
choices2ids = []
aborted = []

@views.route('/')
def home():
    return render_template("index.html")

@views.route('/init')

def startgameconfig():
    global waiting
    global gameidsinuse
    global has1chosen
    global has2chosen
    has1chosen = False
    has2chosen = False
    if waiting == True:
        lastcode = gameidsinuse[-1]
        waiting = False
        return render_template('found.html', lastcode = lastcode)
    happy = False
    while happy == False:                                    #This bit of code checks if a game ID is in use, and gives a code to use
        code = random.randint(1000000, 9999999)
        if code not in gameidsinuse: happy = True
    gameidsinuse.append(code)
    waiting = True
    return render_template('find.html', code = code)          #This peice of code puts the person in queue

@views.route('/ingame/1/<findinggamecode>/<timeremaining>')
def waitingsub(findinggamecode, timeremaining):
    while waiting != False: #Nobody is here
        time.sleep(1)
        return render_template('find.html', code = findinggamecode)
    return render_template('play1.html', findinggamecode = findinggamecode, timeremaining = timeremaining)

@views.route('/ingame/1/<findinggamecode>/<timeremaining>/count')
def counting1(findinggamecode, timeremaining):
    timeremaining = int(timeremaining) - 1
    for item in aborted:
        if item == findinggamecode:
            return('index.html')
    if timeremaining <= 0:
        aborted.append(findinggamecode)
        return render_template('index.html')
    return render_template('play1.html', findinggamecode = findinggamecode, timeremaining = timeremaining)
    

@views.route('/ingame/2/<lastcode>/<timeremaining>')
def joiningsub(lastcode, timeremaining):
    timeremaining = int(timeremaining) - 1
    for item in aborted:
        if item == findinggamecode:
            return render_template('index.html')
    if timeremaining <= 0:
        aborted.append(lastcode)
        return render_template('index.html')
    return render_template('play2.html', lastcode = lastcode, timeremaining = timeremaining)

@views.route('/ingame/1/<lastcode>/playing/<onechoice>')
def chosen1(lastcode, onechoice):    #THIS PEICE OF CODE IS FOR PLAYER 1
    global has2chosen
    global has1chosen
    choices1.append(onechoice)
    choices1ids.append(lastcode)
    choice1 = choices1[-1]

    has1chosen = 1
    if has2chosen ==  1:
        if choices2ids[-1] == lastcode:
            choice2 = choices2[-1]
        else:
            for i in range (1, len(choices2)):
                if choices2ids[i] == lastcode:
                    choice2 = choices2[i]
        if choice2 == choice1:
            return render_template('1draw.html', choice2 = choice2, lastcode = lastcode)
        elif choice2 == 'rock':
            if choice1 == 'paper':
                return render_template('1win.html', choice2 = choice2, lastcode = lastcode)#win
            elif choice1 == 'scissors':
                return render_template('1loose.html', choice2 = choice2, lastcode = lastcode)#loose
        elif choice2 == 'paper':
            if choice1 == 'rock':
                return render_template('1loose.html', choice2 = choice2, lastcode = lastcode)#loose
            elif choice1 == 'scissors':
                return render_template('1win.html', choice2 = choice2, lastcode = lastcode)#win
        elif choice2 == 'scissors':
            if choice1 == 'rock':
                return render_template('1win.html', choice2 = choice2, lastcode = lastcode)#win
            elif choice1 == 'paper':
                return render_template('1loose.html', choice2 = choice2, lastcode = lastcode)#loose
    return render_template('waitingforchocie1.html', choice1 = choice1, lastcode = lastcode)

@views.route('/ingame/2/<findinggamecode>/playing/<twochoice>')
def chosen2(findinggamecode, twochoice):
    global has2chosen
    global has1chosen
    choices2.append(twochoice)
    choices2ids.append(findinggamecode)
    choice2 = twochoice
    has2chosen = 1
    if has1chosen ==  1:
        if choices1ids[-1] == findinggamecode:
            choice1 = choices1[-1]
        else:
            for i in range (1, len(choices2)):
                if choices1ids[i] == findinggamecode:
                    choice1 = choices2[i]
        if choice1 == choice2:
            return render_template('2draw.html', choice1 = choice1, findinggamecode = findinggamecode)#draw
        elif choice1 == 'rock':
            if choice2 == 'paper':
                return render_template('2win.html', choice1 = choice1, findinggamecode = findinggamecode)#win
            elif choice2 == 'scissors':
                return render_template('2loose.html', choice1 = choice1, findinggamecode = findinggamecode)#loose
        elif choice1 == 'paper':
            if choice2 == 'rock':
                return render_template('2loose.html', choice1 = choice1, findinggamecode = findinggamecode)#loose
            elif choice2 == 'scissors':
                return render_template('2win.html', choice1 = choice1, findinggamecode = findinggamecode)#win
        elif choice1 == 'scissors':
            if choice2 == 'rock':
                return render_template('2win.html', choice1 = choice1, findinggamecode = findinggamecode)#win
            elif choice2 == 'paper':
                return render_template('2loose.html', choice1 = choice1, findinggamecode = findinggamecode)#loose
            
    return render_template('waitingforchocie2.html', choice2 = choice2, findinggamecode = findinggamecode)


@views.route('/quit')
def quit():
    global waiting
    waiting = False
    return render_template('quit.html')
