

"""

=> First, I want the script to automatically choose a work, and display the number of chars
=> a screen with a play background
=> on the top left, the word that is going to be filled
=> on the right, the hangman (each part is visible but we can see the diff btwn filled/not filled)
=> bottom left, user letter input (one place to put a letter) + a button

CLASSES:
=> class letter => each letter is a diff object
=> hangman class => each part is a diff object

=> Then, main loop
    => display:
        => word itself (with guessed letters revealed)
        => list of the wrong letter
        => hangman ()
    => ask user for letter
        => if good letter => reveal the places using this letter + display "good letter!"
        => else => add the letter to the wrong letters list + display "oh oh, wrong letter..." + add part to hangman
    
    => IF ENTIRE WORD GUESSED
        => choice between new play/exit
        => if new play
            => re-use the setup/mainloop functions


"""

def chooseWord():
    # put every word of the file into a list
    with open("hangman_wordlist.txt", "r") as file:
        listOfWordsHangman = file.readlines()
        for line in listOfWordsHangman:
            listOfWordsHangman[listOfWordsHangman.index(line)] = line.strip()
    
    from random import randint
    # randomly choose an index in the range of the list of words
    randomIndex = randint(0, len(listOfWordsHangman)-1)
    wordToReturn = listOfWordsHangman[randomIndex]
    while "////" in wordToReturn or ":" in wordToReturn:
        randomIndex = randint(0, len(listOfWordsHangman)-1)
        wordToReturn = listOfWordsHangman[randomIndex]
    i = randomIndex
    # go up until we find the top of the category
    while "////" not in listOfWordsHangman[i]:
        i -=1
    # format the name of the category
    categoryToReturn = ''.join(listOfWordsHangman[i+1].split(':')).strip()
    return wordToReturn, categoryToReturn






# Import and initialize the pygame library
import pygame, os
from time import sleep, time

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_DOWN,
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,)
# from pygame.sprite import _Group

pygame.init()

# get screen size
from sys import platform
if platform == "linux" or platform == "linux2":
    # linux
    screensize = (800, 800)
elif platform == "darwin":
    # OS X
    screensize = (1200, 800)
elif platform == "win32":
    import ctypes
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    # Windows...

# Set up the drawing window
screen = pygame.display.set_mode(screensize)


# set up the size of the font for the letters
wordSize = 30
spaceBTWletters = wordSize*0.93333
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
wordToGuessFont = pygame.font.SysFont('Comic Sans MS', wordSize)

# Calculating spaces between letters
"""numberLetters = 10
keyboardSizeOfLetters = 100
spaceBTWNLetterImages = 10
spaceAtTheLeft = (screensize[0]-((keyboardLetterSize*numLetters)+(spaceLetterImages*(numLetters-1))))/2
spaceLeftatTheLeft = (screensize[0]-((keyboardSizeOfLetters*numberLetters)+((numberLetters-1)*spaceBTWNLetterImages)))/2

print("The width of the screen is: {}px".format(screensize[0]))
print("There are {} images of size {}px, for a total of {}px".format(numberLetters,
                                                                 keyboardSizeOfLetters,
                                                                 (keyboardSizeOfLetters*numberLetters)))
print("There are {} spaces of size {}px, for a total of {}px".format((numberLetters-1),
                                                                       spaceBTWNLetterImages,
                                                                       ((numberLetters-1)*spaceBTWNLetterImages)))
spaceLeftatTheLeft = (screensize[0]-((keyboardSizeOfLetters*numberLetters)+((numberLetters-1)*spaceBTWNLetterImages)))
print(
    "The total of space on the left and right side is {}px,\nSo {}px on the left side".format( spaceLeftatTheLeft, spaceLeftatTheLeft/2)
)"""

# The surface drawn on the screen is now an attribute of 'letter'
class Letter(pygame.sprite.Sprite):
    def __init__(self, x, y:50, index):
        super(Letter, self).__init__()
        self.xPos = x
        self.yPos = y
        self.letter = chosenWord[index].upper()
        self.letterText = wordToGuessFont.render(self.letter, False, (0, 0, 0))
        print("iniatialized letter {} at letter {}".format(index, self.letter))
        # create a text of '_' to display
        self.underscore = wordToGuessFont.render('_', False, (0, 0, 0))
        # var that will serve to know if we need to display the letter or not
        self.hasToDisplay = False
    # display the letter
    def display(self):    
        if self.hasToDisplay:
            screen.blit(self.letterText, (self.xPos, self.yPos))
        # display a dot/underscore instead of the letter
        else:
            screen.blit(self.underscore, (self.xPos, self.yPos))


class hint(pygame.sprite.Sprite):
    def __init__(self, hintGiven, x, y):
        super(hint, self).__init__()

        self.hintFontSize = 40
        self.hintFont = pygame.font.SysFont('Comic Sans MS', self.hintFontSize)
        self.hint = "Hint: " + hintGiven
        print(self.hint)
        self.hintText = self.hintFont.render(self.hint, False, (0, 0, 0))
        self.hintPos = (x, y)
    
    def display(self):
        screen.blit(self.hintText, self.hintPos)





# function which checks when a key is pressed
"""
When a picture of key is pressed:
=> check in the list of all lettersInstances if there are any letters that correspond
=> if so, reveal them
    => after that, make the image pressed green
=> else
    => make the image pressed red
    => take out 1 to the life count
"""
# function runs when a letter THAT CAN BE CLICKED is clicked
def checkKey(letterClickedToCheck: str):
    goodClickedLetter = False
    # it goes through every letter (top left) and if they correspond it reveals them
    for letter in lettersInstances:
        if letter.letter == letterClickedToCheck:
            goodClickedLetter = True
            letter.hasToDisplay = True
    
    # if the letter was good, make the corresponding keyboard letter become green
    if goodClickedLetter:
        letterDict[letterClickedToCheck].becomeGreen()
    # else, make the corresponding keyboard letter become red
    else:
        letterDict[letterClickedToCheck].becomeRed()
        # take out one to the life cound
        global lifeCount
        lifeCount -= 1


# set up keyboard
class keyboardLetter(pygame.sprite.Sprite):
    def __init__(self, x, y, letter):
        super(keyboardLetter, self).__init__()
        # creating the image
        self.letterKey = letter
        print("initializing letter {} of keyboard".format(self.letterKey))
        self.letterImg = pygame.image.load(os.path.join('imageDirectory', 'All_letters', (self.letterKey.upper()+'.png')))
        # Resizing the image, because too big by default
        self.letterImg = pygame.transform.scale(self.letterImg, (keyboardLetterSize, keyboardLetterSize))
        self.rect = self.letterImg.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.letterText = keyboardLetterFont.render(self.letterKey.upper(), False, (0, 0, 0))
        # self.color = (48, 141, 70)
        self.isClickable = True
        # creating the green_tick and red_cross images
        print("initializing gree_tick")
        self.green_tick = pygame.image.load(os.path.join('imageDirectory', 'green_tick.png'))
        # Resizing the green_tick to 1/5 of the letter image
        self.green_tick = pygame.transform.scale(self.green_tick, (keyboardLetterSize/5, keyboardLetterSize/5))
        self.green_tick_rect = self.green_tick.get_rect()
        self.green_tick_rect.x = x
        self.green_tick_rect.y = y
        self.isGreen = False
        print("initializing red_cross")
        self.red_cross = pygame.image.load(os.path.join('imageDirectory', 'red_cross.png'))
        # Resizing the red_cross to the size of the letter image
        self.red_cross = pygame.transform.scale(self.red_cross, (keyboardLetterSize, keyboardLetterSize))
        self.red_cross_rect = self.red_cross.get_rect()
        self.red_cross_rect.x = x
        self.red_cross_rect.y = y
        self.isRed = False
    # display the letter
    def display(self, display: bool):
        # pygame.draw.rect(screen, self.color, pygame.Rect(self.xPosition, # x of top left corner
        #                                                  self.yPosition, # y of top left corner
        #                                                  keyboardLetterSize, # x distance
        #                                                  keyboardLetterSize # y distance
        #                                                  ),  2, 3)
        # screen.blit(self.letterText, (self.xPosition+keyboardLetterSize/7,
        #                               self.yPosition-keyboardLetterSize/20,
        #                               ))
        if display:
            screen.blit(self.letterImg, (self.rect.x, self.rect.y))
            if self.isGreen:
                screen.blit(self.green_tick, (self.green_tick_rect.x, self.green_tick_rect.y))
            elif self.isRed:
                screen.blit(self.red_cross, (self.red_cross_rect.x, self.red_cross_rect.y))
    # check if image was clicked
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    # if we can click it, that is if it has never been clicked
                    if self.isClickable:
                        print(self.letterKey)
                        checkKey(self.letterKey)
    def becomeGreen(self):
        self.isGreen = True
        self.isRed = False
        self.isClickable = False
        self.display(True)
    def becomeRed(self):
        self.isGreen = False
        self.isRed = True
        self.isClickable = False
        self.display(True)
    def reset(self):
        self.isGreen = False
        self.isRed = False
        self.isClickable = True


# heart class, first version with actual hearts
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y, hNum):
        super(Heart, self).__init__()
        self.heartNumber = hNum
        self.isFull = True
        # creating the image
        print("initializing full_heart {}".format(self.heartNumber))
        self.fullHeartImg = pygame.image.load(os.path.join('imageDirectory', 'full_heart.png'))
        print("initializing empty_heart {}".format(self.heartNumber))
        self.emptyHeartImg = pygame.image.load(os.path.join('imageDirectory', 'empty_heart.png'))
        # Resizing the image, because too big by default
        self.fullHeartImg = pygame.transform.scale(self.fullHeartImg, (50, 50))
        self.emptyHeartImg = pygame.transform.scale(self.emptyHeartImg, (50, 50))
        self.rect = self.fullHeartImg.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def display(self):
        if self.isFull:
            screen.blit(self.fullHeartImg, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.emptyHeartImg, (self.rect.x, self.rect.y))

class hangmanPicture(pygame.sprite.Sprite):
    def __init__(self, x, y, hNum):
        super(hangmanPicture, self).__init__()
        self.hangmanPictureNum = hNum
        # creating the image
        print("initializing hangman_picture number {}".format(self.hangmanPictureNum))
        self.hangmanPicture = pygame.image.load(os.path.join('imageDirectory', 'hangman_pictures', str(self.hangmanPictureNum)+'.png'))
        # Resizing the image, because too big by default
        self.hangmanPicture = pygame.transform.scale(self.hangmanPicture, (200, 200))
        self.rect = self.hangmanPicture.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def display(self):
        screen.blit(self.hangmanPicture, (self.rect.x, self.rect.y))  


# menu class
class Menu(pygame.sprite.Sprite):
    def __init__(self):
        super(Menu, self).__init__()
        # creating the image of play
        self.playImg = pygame.image.load(os.path.join('imageDirectory', 'menu', 'play_button.png'))
        self.playButtonSizeX = 467
        self.playButtonSizeY = 152
        self.playImg = pygame.transform.scale(self.playImg, (self.playButtonSizeX, self.playButtonSizeY))
        self.posPlayImg = self.playImg.get_rect()
        self.posPlayImg.x = screensize[0]/2 - self.playButtonSizeX/2
        self.posPlayImg.y = screensize[1]/2 - self.playButtonSizeY/2
        # adding a loading picture
        self.loadingImg = pygame.image.load(os.path.join('imageDirectory', 'menu', 'loading.png'))
        self.loadingSize = 300
        self.loadingImg = pygame.transform.scale(self.loadingImg, (self.loadingSize, self.loadingSize))
        self.posLoading = self.loadingImg.get_rect()
        self.posLoading.x = screensize[0]/2 - self.loadingSize/2
        self.posLoading.y = screensize[1]/2 - self.loadingSize/2
        
    
    def update(self, events, isLoading):
        # still loading, make the loading icon appear
        if isLoading:
            screen.blit(self.loadingImg, self.posLoading)    
            pygame.display.flip()
        # if not loading, make the play button appear
        else:
            screen.blit(self.playImg, self.posPlayImg)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.posPlayImg.collidepoint(event.pos):
                    screen.blit(self.loadingImg, self.posLoading)
                    reset()
    def showWordWhenResetting(self, diedYesOrNo: bool):
        self.wordFontSize = 50

        if diedYesOrNo:
            self.message = "The word was:"
        else:
            self.message = "As you have guessed the word was:"
        self.messageHeading = pygame.font.SysFont('Comic Sans MS', self.wordFontSize).render(self.message, False, (0, 0, 0))
        
        
        screen.blit(self.messageHeading, (screensize[0]/2-((self.wordFontSize*len(self.message))/4), screensize[1]/3))


        self.chosenWordDisplay = pygame.font.SysFont('Comic Sans MS', self.wordFontSize*2).render(chosenWord, False, (0, 0, 0))
        screen.blit(self.chosenWordDisplay, (screensize[0]/2-(self.wordFontSize*len(chosenWord))/2, screensize[1]/3+self.wordFontSize*1.5))


def createWordAndHint():
    
    global wordOffsetX
    wordOffsetX = 100
    global wordOffsetY
    wordOffsetY = 50
    # recreate the letters, as there may not be equal length of word
    global lettersInstances
    lettersInstances = []
    lettersInstances = [Letter(x=i*spaceBTWletters+wordOffsetX, y=150, index=i) for i in range(len(chosenWord))]
    
    # create the hint text
    global hintInstance
    hintInstance = hint(hintGiven=wordCategory, x=60, y=40)

        


def setup():
    # make the menu first
    global menu
    menu = Menu()
    menu.update([], True)
    global isShowingWord
    isShowingWord = False
    global frameCounter
    frameCounter = 0


    global chosenWord, wordCategory
    chosenWord, wordCategory = chooseWord()#"Ablaeidlqmzodhywmddf", "don't"#
        
    global keyboardLetterSize
    keyboardLetterSize = 100
    global spaceLetterImages
    spaceLetterImages = 10
    global keyboardLetterFont
    keyboardLetterFont = pygame.font.SysFont('Helvetica', keyboardLetterSize)

    KEYBOARD = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm'] #['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
    global letterDict
    letterDict = {}

    for row in KEYBOARD:
        numLetters = len(row)
        # Calculating the space there has to be between letters
        spaceLeft = (screensize[0]-((keyboardLetterSize*numLetters)+(spaceLetterImages*(numLetters-1))))/2
        spaceBelow = (screensize[1]/2-(len(KEYBOARD)*keyboardLetterSize))/len(KEYBOARD)
        print("space below:", spaceBelow)
        for letter in row:
            currentLetter = KEYBOARD[KEYBOARD.index(row)][row.index(letter)].upper()
            letterDict[currentLetter] = keyboardLetter(spaceLeft+(row.index(letter)*(keyboardLetterSize+spaceLetterImages)), (screensize[1]/2)+KEYBOARD.index(row)*(keyboardLetterSize+spaceBelow), currentLetter.upper())
            print("current letter:", currentLetter)
        # for letter
    
    createWordAndHint()


    # add a life var
    global lifeCount, maxLife
    maxLife = 11
    lifeCount = maxLife #5#

    # create heart instances
    global heartInstances
    heartInstances = []
    heartInstances = [Heart(i*60+800, 50, i) for i in range(maxLife)]

    # create hangman pictures instances
    global hangmanPictureInstances
    hangmanPictureInstances = []
    hangmanPictureInstances = [hangmanPicture(800, 100, i) for i in range(maxLife+1)]
    print("number of hangman pictures:", len(hangmanPictureInstances))
    print("last element of hangmanPictureInstances:", hangmanPictureInstances[len(hangmanPictureInstances)-1].hangmanPictureNum)

def reset():

    global mainLoop
    mainLoop = True
    global isShowingWord
    isShowingWord = False
    global timeCounter
    timeCounter = 0
    global frameCounter
    frameCounter = 0
    # setup()
    
    global chosenWord, wordCategory
    chosenWord, wordCategory = chooseWord()#"Ablaeidlqmzodhywmddf"#

    # reset default values of keyboard letters
    for letter in letterDict:
        letterDict[letter].reset()


    createWordAndHint()
    

    # reset life count
    global lifeCount
    lifeCount = maxLife


def displayHearts():
    for heart in heartInstances:
        if heartInstances.index(heart) >= lifeCount:
            heart.isFull = False
        else:
            heart.isFull = True
        heart.display()

def displayKeyboard(hasToDisplay: bool):
    for letter in letterDict:
        letterDict[letter].update(events)
        letterDict[letter].display(hasToDisplay)






# choose word and create keyboard + hidden letters
global lifeCount
global timeCounter
timeCounter = 0
setup()

global heartsOrHangman
heartsOrHangman = False

# text_surface = my_font.render('Some Text', False, (0, 0, 0))

# Run until the user asks to quit
running = True
mainLoop = False
background = pygame.image.load(os.path.join('imageDirectory', 'background.jpg'))
background = pygame.transform.scale(background, screensize)

limitOfLetters = len(lettersInstances)/2

while running:

    # put a background
    screen.blit(background, (0, 0))

    # get all the events
    
    global events
    events = pygame.event.get()

    # Look at every event in the queue
    for event in events:
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    if mainLoop:
        
        # display the keyboard
        displayKeyboard(True)

        # display hearts
        if heartsOrHangman:
            displayHearts()
        
        # display the hangman pictures
        try:
            hangmanPictureInstances[maxLife-lifeCount].display()
        except:
            print("couldn't print the hangman picture, the index is:", maxLife-lifeCount)
            hangmanPictureInstances[11].display()
    
    
        # display the word to guess
        gameWasWon = True
        for letter in lettersInstances:
            letter.display()
            if not letter.hasToDisplay:
                gameWasWon = False

        # display the hint
        hintInstance.display()
        
        if gameWasWon and frameCounter == 0:
            frameCounter = 1
        elif gameWasWon and frameCounter != 0:
            print("you won")
            print("The word was:", chosenWord)
            isShowingWord = True
            died = False
            mainLoop = False
            timeCounter = time()
            # frameCounter = 0 so that next time someone wins, he will wait one frame until printing "you won"
            frameCounter = 0
            sleep(2)
            # reset()
            
        if lifeCount <= 0 and frameCounter == 0:
            frameCounter = 1
        elif lifeCount <= 0 and frameCounter != 0:
            print("you died")
            print("The word was:", chosenWord)
            isShowingWord = True
            died = True
            mainLoop = False
            timeCounter = time()
            # frameCounter = 0 so that next time someone loses, he will wait one frame until printing "you won"
            frameCounter = 0
            sleep(2)
            # exit(0)

    elif isShowingWord == True:
        menu.showWordWhenResetting(died)
        if time()-timeCounter > 8: # if more than 8 seconds elapsed
            isShowingWord = False
        # sleep 8 seconds before resetting the game

    else:

        menu.update(events, False)

    # Flip the display SUPER IMPORTANT!!!!!
    pygame.display.flip()


# Done! Time to quit.

pygame.quit()

