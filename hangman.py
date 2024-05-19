
import os
from time import sleep
from random import randint

def chooseWord():
    # put every word of the file into a list
    with open("hangman_wordlist.txt", "r") as file:
        listOfWordsHangman = file.readlines()
        for line in listOfWordsHangman:
            listOfWordsHangman[listOfWordsHangman.index(line)] = line.strip()
    
    # randomly choose an index in the range of the list of words
    randomIndex = randint(0, len(listOfWordsHangman)-1)
    while '////' in listOfWordsHangman[randomIndex] or ':' in listOfWordsHangman[randomIndex]:
        randomIndex = randint(0, len(listOfWordsHangman)-1)
    
    wordToReturn = listOfWordsHangman[randomIndex]
    i = randomIndex
    # go up until we find the top of the category
    while "////" not in listOfWordsHangman[i]:
        i -=1
    # take out spaces and ':' from the name of the category
    categoryToReturn = ''.join(listOfWordsHangman[i+1].split(':')).strip()
    return wordToReturn, categoryToReturn

# function to clear screen
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def printHangman():
    cls()
    size = os.get_terminal_size()
    titleMessage = "MY AMAZING HANGMAN GAME"
    titleBorders = (size.columns-len(titleMessage))/2
    print("\n" + "*"*int(titleBorders) + titleMessage + "*"*int(titleBorders))
    print("\n")
    numLivesMax = 7
    if livesLefts < numLivesMax:
        print("")
        if livesLefts < (numLivesMax-1):
            print("    ---------------------------")
        if livesLefts < (numLivesMax-2):
            print("   |  /                       |")
        else:
            if livesLefts < (numLivesMax-1):
                print("   |  /")
            else:
                print("   |")
        if livesLefts < (numLivesMax-3):
            print("   | /                        O")
        else:
            if livesLefts < (numLivesMax-1):
                print("   | /")
            else:
                print("   |")
        if livesLefts < (numLivesMax-4):
            if livesLefts < (numLivesMax-5):
                print("   |/                        _|_")
            else:
                print("   |/                         |")
        else:
            if livesLefts < (numLivesMax-1):
                print("   |/")
            else:
                print("   |")
    # else:
    
    if livesLefts < (numLivesMax-4):
        print("   |                          |")
    else:
        if livesLefts < numLivesMax:
            print("   |")
    
    if livesLefts < (numLivesMax-6):
        print("   |                         / \\")
        print("   |")
        print("   |")
    else:
        if livesLefts < numLivesMax:
            print("   |")
            print("   |")
            print("   |")
        else:
            print("")
            print("")
            print("")
    print("-------")


def checkLetter(letterToCheck):
    if letterToCheck in wordChosen:
        # if the letter is a good guess
        for i in range(len(wordChosen)):
            # if the letter to check is in the chosen word, then insert the letter in the string to display
            if wordChosen[i] == letterToCheck:
                # replace the old "_" value with the letter
                global stringToDisplay
                stringToDisplay = stringToDisplay[:i] + letterToCheck + stringToDisplay[i + 1:]
        return True
    else:
        global livesLefts
        livesLefts -= 1
        listOfWrongLetters.append(userInput)
        return False

# This will print the word partially (only guessed letters) AND the list of tested letters
def printStats():
    print("\n\nHint: category of word={}".format(wordCategory))
    print("\n\nCAN YOU GUESS THE HIDDEN LETTERS?: {} (remaining lifes={})".format(stringToDisplay, livesLefts))
    if listOfWrongLetters:
        print("\nTested Letters:", ' '.join(listOfWrongLetters))

def checkIfGoodInput():
    if not userInput:
        return "\nYou have to input a letter!"
    elif len(userInput) > 1:
        return "\nYou must enter a letter, not a word!"
    elif not userInput.isalpha():
        return "\nYou must enter a letter, not any other type of characters!"
    elif userInput in listOfWrongLetters or userInput in stringToDisplay:
        return "\nIt seems like you already tried this one"
    return None



"""

=> reset() => get a word, reset variables, set gameLoop to True

"""

def reset():
    global wordChosen, wordCategory
    wordChosen, wordCategory = chooseWord()
    # mainloop means program is running
    global mainloop
    mainloop = True
    # gameLoop means hangman is currently being played
    global gameLoop
    gameLoop = True
    # number of lives by default: 7
    global livesLefts
    livesLefts = 7
    
    global userInput
    userInput = '1' # setting the var to a number to know if the var was just initialized or not

    # the printed word, containing the guessed letters and the not guessed letters as "_"
    global stringToDisplay
    stringToDisplay = len(wordChosen)*"_"

    # list that will contain the letters that were tested and WRONG
    global listOfWrongLetters
    listOfWrongLetters = []

    print("***************LET'S PLAY HANGMAN!!!***************")



global livesLefts
livesLefts = 7

# printHangman(10)
# sleep(2)
# printHangman(9)
# sleep(2)
# printHangman(8)
# sleep(2)
# printHangman(7)
# sleep(2)
# printHangman(6)
# sleep(2)
# printHangman(5)
# sleep(2)
# printHangman(4)
# sleep(2)
# printHangman(3)
# sleep(2)
# printHangman(2)
# sleep(2)
# printHangman(1)
# sleep(2)
# printHangman(0)

"""
=> print the hangman
=> say if the user input was good or not
=> print the word to guess (with already done letters)
=> let the user input a letter

"""

reset()

while mainloop:
    if gameLoop:

        
        # check if the input is a letter and only one
        isInvalidInput = checkIfGoodInput()
        isCorrectLetter = False
        if not isInvalidInput:
            isCorrectLetter = checkLetter(userInput)
        
        printHangman()


        # Then, print:
        #   => the word with the guessed letters displayed, the others displayed as "_"
        #   => the list of tested letters
        printStats()


        # printing the messages
        if isInvalidInput:
            print(isInvalidInput)
        else:
            if isCorrectLetter:
                print("\nGood guess!, you guessed the letter", userInput)
            else:
                print("\nOh oh, bad guess...")
        
        

        
        if livesLefts == 0:
            print("\n\nOh oh, looks like you just lost...")
            print("\nThe word was:", wordChosen.upper())
            gameLoop = False
            continue
        elif "_" not in stringToDisplay:
            print("\n\nYOUHOUHOU! YOU WON!")
            gameLoop = False
            continue

        # ASK FOR USER INPUT
        userInput = input("\nPlease enter a valid letter:").strip()

    else:
        answer = input("\nDo you want to play again? (y/N)")
        while answer.lower() != "y" and answer.lower() != "n":
            answer = input("\nDo you want to play again? (y/N)")
        if answer.lower() == "y":
            print("******************recreating game...******************")
            reset()
        else:
            print("\nexiting")
            exit(0)
        # sleep(1)
        # print("don't know what to do...")
        


