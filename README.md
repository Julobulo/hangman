# Hangman Game with Pygame

## Overview

Welcome to the Hangman game implemented using Pygame! This project is a graphical version of the classic word-guessing game. The goal is to guess the word by suggesting letters within a certain number of guesses.

## Features

- Automatically chooses a word from a provided list.
- Displays a play screen with a background, the word to guess, and a hangman figure.
- Tracks guessed and incorrect letters, updating the display accordingly.
- Provides a graphical user interface for user input.
- Allows for replaying the game after winning or losing.

## Installation

1. Ensure you have Python installed on your system. This project is compatible with Python 3.
2. Install Pygame using pip:
   ```bash
   pip install pygame
   ```
3. Download or clone this repository to your local machine.

## Files

- `hangman.py`: The main script to run the game.
- `hangman_wordlist.txt`: A text file containing the list of words to be used in the game.
- `imageDirectory`: A folder containing images for the game including letters, hangman parts, and other UI elements.

## Usage

To start the game, run the following command in your terminal:
```bash
python hangman.py
```

## Game Instructions

1. **Start the Game**: Upon running the script, you will see a play button. Click the play button to start the game.
2. **Guess the Word**: Use the on-screen keyboard to guess the letters in the word. 
   - Correct guesses reveal the letter in the word.
   - Incorrect guesses add a part to the hangman.
3. **Winning the Game**: If you guess all the letters in the word correctly before the hangman is fully drawn, you win.
4. **Losing the Game**: If the hangman is fully drawn before you guess the word, you lose.
5. **Play Again**: After winning or losing, you will have the option to play again or exit the game.

## Classes and Main Loop

### `Letter` Class
Represents each letter in the word to guess.
- **Attributes**:
  - `xPos`, `yPos`: Position of the letter.
  - `letter`: The actual letter.
  - `letterText`: Rendered text of the letter.
  - `underscore`: Rendered text of the underscore.
  - `hasToDisplay`: Boolean indicating if the letter should be displayed.

### `Hint` Class
Displays the hint for the word.
- **Attributes**:
  - `hintGiven`: The hint text.
  - `hintText`: Rendered text of the hint.
  - `hintPos`: Position of the hint.

### `KeyboardLetter` Class
Represents each letter in the on-screen keyboard.
- **Attributes**:
  - `letterKey`: The letter itself.
  - `letterImg`: Image of the letter.
  - `rect`: Rectangle for collision detection.
  - `isClickable`: Boolean indicating if the letter can be clicked.
  - `isGreen`, `isRed`: Booleans indicating the letter's status.

### `HangmanPicture` Class
Represents the hangman image.
- **Attributes**:
  - `hangmanPictureNum`: The number of the hangman picture.
  - `hangmanPicture`: The image of the hangman picture.
  - `rect`: Rectangle for positioning.

### `Menu` Class
Handles the main menu of the game.
- **Attributes**:
  - `playImg`: Image of the play button.
  - `loadingImg`: Image of the loading screen.
  - `posPlayImg`, `posLoading`: Positions of the images.

### Main Loop

The main loop handles:
- Displaying the background and current state of the game.
- Processing user input.
- Updating the game state (checking for correct/incorrect guesses).
- Displaying messages for winning or losing.
- Offering the option to replay or exit the game.

## Contributions

Contributions are welcome! Feel free to submit issues or pull requests to improve the game.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

Enjoy the game!