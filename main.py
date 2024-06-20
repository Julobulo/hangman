import asyncio
import math
"""
First, I want the script to automatically choose a work, and display the number of chars a screen with a play background
on the top left, the word that is going to be filled on the right, the hangman top right, user letter input (one place to put a letter).

CLASSES:
Class letter: Each letter is a different object.
Hangman class: Each part is a different object.

Then, main loop:
    Display:
        word itself (with guessed letters revealed).
        List of the wrong letter.
        hangman()
    Ask user for letter:
        If good letter: Reveal the places using this letter.
        Else: Add the letter to the wrong letters list and add part to hangman.
    
    If entire word guessed:
        Choice between new play/exit:
        If new play:
            Re-use the setup/mainloop functions.
"""





# Import PYGAME LIBRARY to put all the elements in the canvas.
import pygame
# Import OS LIBRARY to use the list in an easier way.
import os
# Import PYGAME.LOCALS for easier access to key coordinates
from pygame.locals import ( K_ESCAPE, KEYDOWN, QUIT, K_q )
# Import CYTIPES LIBRARY to get length in a Windows computer.
import ctypes
# Import SYS LIBRARY to get information about each plataform.
from sys import platform
# Inport RANDOM LIBRARY to get the random word from the list.
from random import randint
# Import TIME LIBRARY to give the user some time between every output.
from time import sleep, time

async def main():
# def main():
    # Set the screen and the letter size. 
    # Linux.
    global screensize
    # if platform == "linux" or platform == "linux2": # <= SYS LIBRARY
    #     screensize = (800, 800)
    #     print('You are on linux')
    # # OS X.
    # elif platform == "darwin": # <= SYS LIBRARY
    #     screensize = (1200, 800)
    #     print('You are on OS X')
    # # Windows.
    # elif platform == "win32": # <= SYS LIBRARY
    #     user32 = ctypes.windll.user32 # <= CYTIPES LIBRARY
    #     screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    #     print('You are on windows')
    # else:
    #     screensize = (800, 800)
    screensize = (640, 500)
    global factor
    factor = (screensize[0]/1400) # it reduces or grows everything's size approximately depending on the screen size
    
    # Set up the drawing window.
    screen = pygame.display.set_mode(screensize) # <= PYGAME LIBRARY
    pygame.display.set_caption("Hangman game made with pygame") # <= set screen/tab caption

    # Set up the size of the font for the letters.
    wordSize = 30
    spaceBTWletters = wordSize * 0.93333 * factor
    pygame.font.init()
    wordToGuessFont = pygame.font.SysFont('Comic Sans MS', math.floor(wordSize))

    # Letter class, each letter on the screen is an object of this class
    class Letter(pygame.sprite.Sprite):
        def __init__(self, x, y: 50, index):
            super(Letter, self).__init__()
            self.letter = chosenWord[index].upper()
            self.letterText = wordToGuessFont.render(self.letter, False, (0, 0, 0))
            letterA_rect = wordToGuessFont.render("a", False, (0, 0, 0)).get_rect()
            letter_x = screensize[0]/4 - letterA_rect.width/2 - (letterA_rect.width + spaceBTWletters) * ( (len(chosenWord) - 1)/2 - index )
            self.xPos = letter_x
            self.yPos = y - math.floor(100 * factor)
            # Create a text of '_' to display.
            self.underscore = wordToGuessFont.render('_', False, (0, 0, 0))
            # Variable that will allows us to know if we need to display the letter or the underscore
            self.hasToDisplay = False
        # Display the letter.
        def display(self):    
            if self.hasToDisplay:
                screen.blit(self.letterText, (self.xPos, self.yPos))
            # Display a underscore instead of the letter.
            else:
                screen.blit(self.underscore, (self.xPos, self.yPos))

    # Class for the hint that will tell us what type of word it is (We use the same procedure/logic like in the Letter class).
    class hint(pygame.sprite.Sprite):
        def __init__(self, hintGiven, x, y):
            super(hint, self).__init__()

            # Select the size for the letters to adapt it to our needs.
            self.hintFontSize = math.floor(40 * factor)
            self.hintFont = pygame.font.SysFont('Comic Sans MS', self.hintFontSize) # <= PYGAME LIBRARY
            self.hint = "Hint: " + hintGiven
            print(self.hint)
            self.hintText = self.hintFont.render(self.hint, False, (0, 0, 0))
            hint_rect = self.hintText.get_rect()
            hint_x = ((screensize[0]/2 - hint_rect.width) / 2)
            self.hintPos = (hint_x, math.floor(y * factor))
        def display(self):
            screen.blit(self.hintText, self.hintPos) # <= PYGAME LIBRARY


    # Set up keyboard.
    class keyboardLetter(pygame.sprite.Sprite):
        def __init__(self, x, y, letter):
            super(keyboardLetter, self).__init__()
            
            # Creating the image.
            self.letterKey = letter
            print(f"initializing letter {self.letterKey} of keyboard")
            self.letterImg = pygame.image.load(os.path.join('imageDirectory', 'All_letters', (self.letterKey.upper() + '.png'))) # <= PYGAME/OS LIBRARY
            # Resizing the image, because too big by default.
            self.letterImg = pygame.transform.scale(self.letterImg, (keyboardLetterSize, keyboardLetterSize)) # <= PYGAME LIBRARY
            self.rect = self.letterImg.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.isClickable = True
            # Creating the green_tick and red_cross images.
            self.green_tick = pygame.image.load(os.path.join('imageDirectory', 'green_tick.png')) # <= PYGAM/OS LIBRARY
            # Resizing the green_tick to 1/5 of the letter image.
            self.green_tick = pygame.transform.scale(self.green_tick, (keyboardLetterSize / 5, keyboardLetterSize / 5)) # <= PYGAME LIBRARY
            self.green_tick_rect = self.green_tick.get_rect()
            self.green_tick_rect.x = x
            self.green_tick_rect.y = y
            self.isGreen = False
            self.red_cross = pygame.image.load(os.path.join('imageDirectory', 'red_cross.png')) # <= PYGAME/OS LIBRARY
            # Resizing the red_cross to the size of the letter image.
            self.red_cross = pygame.transform.scale(self.red_cross, (keyboardLetterSize, keyboardLetterSize)) # <= PYGAME LIBRARY
            self.red_cross_rect = self.red_cross.get_rect()
            self.red_cross_rect.x = x
            self.red_cross_rect.y = y
            self.isRed = False
        # Display the letter.
        def display(self, display: bool):
            if display:
                screen.blit(self.letterImg, (self.rect.x, self.rect.y)) # <= Print letter to screen
                if self.isGreen:
                    screen.blit(self.green_tick, (self.green_tick_rect.x, self.green_tick_rect.y)) # <= print green tick to screen
                elif self.isRed:
                    screen.blit(self.red_cross, (self.red_cross_rect.x, self.red_cross_rect.y)) # <= print red cross to screen
        # Check if image was clicked.
        def update(self, events):
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP: # <= PYGAME LIBRARY
                    if self.rect.collidepoint(event.pos):
                        print(f'{self.letterKey} got clicked')
                        # If we can click it, that is if it has never been clicked.
                        if self.isClickable:
                            print(self.letterKey)
                            checkKey(self.letterKey)
        # If the letter was the right one
        def becomeGreen(self):
            self.isGreen = True
            self.isRed = False
            self.isClickable = False
            self.display(True)
        # If the letter was the wrong one
        def becomeRed(self):
            self.isGreen = False
            self.isRed = True
            self.isClickable = False
            self.display(True)
        # Once the game is over ad we want to reset all the letters
        def reset(self):
            self.isGreen = False
            self.isRed = False
            self.isClickable = True


    # Class used to render the hangman picture.
    class hangmanPicture(pygame.sprite.Sprite):
        def __init__(self, x, y, hNum):
            super(hangmanPicture, self).__init__()
            self.hangmanPictureNum = hNum
            # Creating the image.
            self.hangmanPicture = pygame.image.load(os.path.join('imageDirectory', 'hangman_pictures', str(self.hangmanPictureNum) + '.png')) # <= PYGAME/OS LIBRARY
            # Resizing the image, because too big by default.
            self.hangmanPicture = pygame.transform.scale(self.hangmanPicture, (200 * factor, 200 * factor)) # <= PYGAME LIBRARY
            self.rect = self.hangmanPicture.get_rect()
            self.rect.x = x
            self.rect.y = y
        # Display the image.
        def display(self):
            screen.blit(self.hangmanPicture, (self.rect.x, self.rect.y)) # <= PYGAME LIBRARY


    # Menu class is used to display everything and also to upload the code after every input.
    class Menu(pygame.sprite.Sprite):
        def __init__(self):
            super(Menu, self).__init__()
            # Creating the image of play.
            self.playImg = pygame.image.load(os.path.join('imageDirectory', 'menu', 'play_button.png')) # <= PYGAME/OS LIBRARY
            self.playButtonSizeX = math.floor(467 * factor)
            self.playButtonSizeY = math.floor(152 * factor)
            self.playImg = pygame.transform.scale(self.playImg, (self.playButtonSizeX, self.playButtonSizeY)) # <= PYGAME LIBRARY
            self.posPlayImg = self.playImg.get_rect()
            self.posPlayImg.x = (screensize[0] / 2) - (self.playButtonSizeX / 2)
            self.posPlayImg.y = (screensize[1] / 2) - (self.playButtonSizeY / 2)
            # Adding a loading picture.
            self.loadingImg = pygame.image.load(os.path.join('imageDirectory', 'menu', 'loading.png')) # <= PYGAME/OS LIBRARY
            self.loadingSize = math.floor(300 * factor)
            self.loadingImg = pygame.transform.scale(self.loadingImg, (self.loadingSize, self.loadingSize)) # <= PYGAME LIBRARY
            self.posLoading = self.loadingImg.get_rect()
            self.posLoading.x = (screensize[0] / 2) - (self.loadingSize / 2)
            self.posLoading.y = (screensize[1] / 2) - (self.loadingSize / 2)
        def update(self, events, isLoading):
            # Still loading, make the loading icon appear.
            if isLoading:
                screen.blit(self.loadingImg, self.posLoading)    
                pygame.display.flip()
            # If not loading, make the play button appear.
            else:
                screen.blit(self.playImg, self.posPlayImg)
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP: # <= PYGAME LIBRARY
                    if self.posPlayImg.collidepoint(event.pos):
                        screen.blit(self.loadingImg, self.posLoading) # <= PYGAME LIBRARY
                        reset()
        # Once the game is over, we want to show the word that we were looking for.
        def showWordWhenResetting(self, diedYesOrNo: bool):
            self.wordFontSize = math.floor(50 * factor)
            if diedYesOrNo:
                self.message = "The word was:"
            else:
                self.message = "As you have guessed the word was:"
            # Show message (w/o word)
            self.messageHeading = pygame.font.SysFont('Comic Sans MS', self.wordFontSize).render(self.message, False, (0, 0, 0)) # <= PYGAME LIBRARY
            text_rect = self.messageHeading.get_rect()
            # Calculate the position to center the text
            text_x = (screensize[0] - text_rect.width) / 2
            screen.blit(self.messageHeading, (text_x, screensize[1] / 3)) # <= PYGAME LIBRARY
            # Show word
            self.chosenWordDisplay = pygame.font.SysFont('Comic Sans MS', self.wordFontSize*2).render(chosenWord, False, (0, 0, 0)) # <= PYGAME LIBRARY
            word_rect = self.chosenWordDisplay.get_rect()
            # Calculate the position to center the text
            word_x = (screensize[0] - word_rect.width) / 2
            screen.blit(self.chosenWordDisplay, (word_x, (screensize[1] / 3) + (self.wordFontSize * 1.5)))


    # Choose a random word from our list of words.
    def chooseWord():
        # Put every word of the file into a list.
        with open("hangman_wordlist.txt", "r") as file:
            listOfWordsHangman = file.readlines()
            for line in listOfWordsHangman:
                listOfWordsHangman[listOfWordsHangman.index(line)] = line.strip()
        # Randomly choose an index in the range of the list of words.
        randomIndex = randint(0, len(listOfWordsHangman) - 1)
        wordToReturn = listOfWordsHangman[randomIndex]
        while "////" in wordToReturn or ":" in wordToReturn:
            randomIndex = randint(0, len(listOfWordsHangman) - 1)
            wordToReturn = listOfWordsHangman[randomIndex]
        i = randomIndex
        # Go up until we find the top of the category.
        while "////" not in listOfWordsHangman[i]:
            i -=1
        # Format the name of the category.
        categoryToReturn = ''.join(listOfWordsHangman[i + 1].split(':')).strip()
        return wordToReturn, categoryToReturn


    # Function runs when a letter (that can be clicked) is clicked.
    def checkKey(letterClickedToCheck: str):
        goodClickedLetter = False
        # It goes through every letter (from the word that we are looking for) and if they correspond it reveals them.
        for letter in lettersInstances:
            if letter.letter == letterClickedToCheck:
                goodClickedLetter = True
                letter.hasToDisplay = True
        # If the letter was good, make the corresponding keyboard letter become green.
        if goodClickedLetter:
            letterDict[letterClickedToCheck].becomeGreen()
        # Else, make the corresponding keyboard letter become red.
        else:
            letterDict[letterClickedToCheck].becomeRed()
            # Take out one to the life count.
            global lifeCount
            lifeCount -= 1


    # Global variables related with the letters.
    def createWordAndHint():
        global wordOffsetX
        wordOffsetX = 100
        global wordOffsetY
        wordOffsetY = 50
        # Recreate the letters, as there may not be equal length of word.
        global lettersInstances
        lettersInstances = []
        lettersInstances = [Letter(x = i * spaceBTWletters + wordOffsetX, y = 150, index = i) for i in range(len(chosenWord))]
        # Create the hint text.
        global hintInstance
        hintInstance = hint(hintGiven = wordCategory, x = 60, y = 40)


    # Global variables related with the keybooard.
    def setup():
        # Nake the menu first.
        global menu
        menu = Menu()
        menu.update([], True)

        global mainLoop
        mainLoop = True

        global isShowingWord
        isShowingWord = False

        global timeCounter
        timeCounter = 0

        global frameCounter
        frameCounter = 0

        global chosenWord, wordCategory
        chosenWord, wordCategory = chooseWord()
            
        global keyboardLetterSize
        keyboardLetterSize = math.floor(100 * factor)

        global spaceLetterImages
        spaceLetterImages = 10

        global keyboardLetterFont
        keyboardLetterFont = pygame.font.SysFont('Helvetica', keyboardLetterSize) # <= PYGAME LIBRARY

        KEYBOARD = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
        global letterDict
        letterDict = {}

        for row in KEYBOARD:
            numLetters = len(row)
            
            # Calculating the space there has to be between letters.
            spaceLeft = (screensize[0] - ((keyboardLetterSize * numLetters) + (spaceLetterImages * (numLetters - 1)))) / 2
            spaceBelow = ((screensize[1] / 2) - (len(KEYBOARD) * keyboardLetterSize)) / len(KEYBOARD)
            print("space below:", spaceBelow)
            for letter in row:
                currentLetter = KEYBOARD[KEYBOARD.index(row)][row.index(letter)].upper()
                letterDict[currentLetter] = keyboardLetter(spaceLeft + (row.index(letter) * (keyboardLetterSize + spaceLetterImages)), (screensize[1] / 2) + KEYBOARD.index(row) * (keyboardLetterSize + spaceBelow), currentLetter.upper())
                print("current letter:", currentLetter)
        
        createWordAndHint()

        # Add a life var.
        global lifeCount, maxLife
        maxLife = 11
        lifeCount = maxLife

        # Create hangman pictures instances.
        global hangmanPictureInstances
        hangmanPictureInstances = []
        hangmanPictureInstances = [hangmanPicture(800 * factor, 100 * factor, i) for i in range(maxLife + 1)]
        print("number of hangman pictures:", len(hangmanPictureInstances))
        print("last element of hangmanPictureInstances:", hangmanPictureInstances[len(hangmanPictureInstances) - 1].hangmanPictureNum)





    # Global variables related with the menu.
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
        chosenWord, wordCategory = chooseWord()

        # Reset default values of keyboard letters.
        for letter in letterDict:
            letterDict[letter].reset()

        createWordAndHint()
        
        # Reset life count.
        global lifeCount
        lifeCount = maxLife





    # Display the Keyboard.
    def displayKeyboard(hasToDisplay: bool):
        for letter in letterDict:
            letterDict[letter].update(events)
            letterDict[letter].display(hasToDisplay)





    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("NOOOOOOO")
    pygame.init()

    # Initiate the library.
    pygame.init() # <= PYGAME LIBRARY

    # Choose word and create keyboard and the hidden letters.
    global lifeCount
    global timeCounter

    timeCounter = 0
    setup()


    # Run until the user asks to quit.
    global running
    running = True
    global mainLoop
    mainLoop = False
    background = pygame.image.load(os.path.join('imageDirectory', 'background.jpg')) # <= PYGAME/OS LIBRARY
    # background = pygame.image.load('./background.jpg')
    background = pygame.transform.scale(background, screensize) # <= PYGAME LIBRARY

    limitOfLetters = len(lettersInstances) / 2


    global isShowingWord
    global frameCounter
    while running:

        # Put a background.
        screen.blit(background, (0, 0))

        # Get all the events.
        global events
        events = pygame.event.get() # <= PYGAME LIBRARY

        # Look at every event in the queue.
        for event in events:
            # If th euser hits the key.
            if event.type == KEYDOWN:
                # If ESCAPE, stop the loop.
                if event.key == K_ESCAPE:
                    running = False
            # If WINDOW, stop the loop.
            elif event.type == QUIT:
                running = False

        if mainLoop:
            
            # Display the keyboard.
            displayKeyboard(True)
            
            # Display the hangman pictures.
            try:
                if maxLife-lifeCount != 0:
                    hangmanPictureInstances[maxLife-lifeCount].display()
            except:
                print("couldn't print the hangman picture, the index is:", maxLife - lifeCount)
                hangmanPictureInstances[11].display()
        
        
            # Display the word to guess.
            gameWasWon = True
            for letter in lettersInstances:
                letter.display()
                if not letter.hasToDisplay:
                    gameWasWon = False

            # Display the hint.
            hintInstance.display()
            
            if gameWasWon and frameCounter == 0:
                frameCounter = 1
            elif gameWasWon and frameCounter != 0:
                print("you won")
                print("The word was:", chosenWord)
                
                isShowingWord = True
                died = False
                mainLoop = False
                
                # The program will wait for a little bit after either winning or loosing.
                timeCounter = time() # <= TIME LIBRARY
                frameCounter = 0
                sleep(2) # <= TIME LIBRARY
                
            if lifeCount <= 0 and frameCounter == 0:
                frameCounter = 1
            elif lifeCount <= 0 and frameCounter != 0:
                print("you died")
                print("The word was:", chosenWord)

                isShowingWord = True
                died = True
                mainLoop = False
                
                # The program will wait for a little bit after either winning or loosing.           
                timeCounter = time() # <= TIME LIBRARY
                frameCounter = 0
                sleep(2) # <= TIME LIBRARY

        elif isShowingWord == True:
            menu.showWordWhenResetting(died)
            
            # Wait for 5 seconds.
            if time() - timeCounter > 5: 
                isShowingWord = False

        else:
            menu.update(events, False)
        
        
        # screen.fill((0, 0, 0))  # Fill the screen with black
        # pygame.draw.rect(screen, (0, 0, 255), (100, 100, 50, 50))  # Draw a blue square

        # Displays all the elements that we put in the canvas with the function screen.blit()
        pygame.display.flip() # <= PYGAME LIBRARY
        
        await asyncio.sleep(0)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # screen.fill((0, 0, 0))  # Fill the screen with black
        # pygame.draw.rect(screen, (0, 0, 255), (100, 100, 50, 50))  # Draw a blue square

        pygame.display.flip()

        await asyncio.sleep(0)  # Non-blocking delay
        


    # If the loop is over then is time to finish the game.
    pygame.quit() # <= PYGAME LIBRARY


    pygame.quit()



asyncio.run(main())
# main()