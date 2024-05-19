

from random import randint


def chooseWord():
    # put every word of the file into a list
    with open("hangman_wordlist.txt", "r") as file:
        listOfWordsHangman = [line.strip() for line in file.readlines()]
    
    # randomly choose an index in the range of the list of words
    randomIndex = randint(0, len(listOfWordsHangman)-1)
    while '////' in listOfWordsHangman[randomIndex] or ':' in listOfWordsHangman[randomIndex]:
        randomIndex = randint(0, len(listOfWordsHangman)-1)
    
    wordToReturn = listOfWordsHangman[randomIndex]

    i = randomIndex
    # go up until we find the top of the category, that is '////'
    while "////" not in listOfWordsHangman[i]:
        i -=1
    
    # take out ':' from the name of the category
    categoryToReturn = listOfWordsHangman[i+1].split(':')[0]

    return wordToReturn, categoryToReturn

chosenWordTuple = chooseWord()
print("a" + chosenWordTuple[0] + "b" + chosenWordTuple[1] + "c")