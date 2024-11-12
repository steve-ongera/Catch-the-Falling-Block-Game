# Catch the Falling Block Game

## Description
Catch the Falling Block is an exciting game where you control a basket to catch falling blocks. Each block has a different score value depending on its color. The goal is to catch as many blocks as possible while avoiding missing too many. If you miss too many blocks, the game ends.

After the game ends, your score is saved to a local SQLite database, and you can view your previous scores.

## Features
- Falling blocks with different colors and score values.
- A basket controlled by the player to catch blocks.
- The game ends when a certain number of blocks are missed.
- Game-over screen showing your score.
- Options to play again or quit.
- Button to view previous scores saved in the database.
- Automatically saves your score to a database after each game.

## Requirements
- Python 3.6 or later
- Pygame
- SQLite (for score storage)

## Installation

1. **Install Pygame**:
   To install Pygame, run the following command:

  - pip install pygame

Clone the Repository: Clone the repository to your local machine:

bash
Copy code
git clone https://github.com/yourusername/catch-the-falling-block.git
Run the Game: Navigate to the project directory and run the game using the following command:


python game.py

## How to Play
- Use the left arrow key to move the basket left.
- Use the right arrow key to move the basket right.
- Catch as many blocks as you can to earn points.
- If you miss too many blocks, the game ends.
- After the game ends, you can choose to Play Again, Quit, or View Previous Scores.

## Database
The game uses a local SQLite database (game_scores.db) to store player scores. The database is automatically created when the game is run for the first time.

The database schema is as follows:

CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY,
    player_name TEXT,
    score INTEGER
);


Scores are saved under the player name "Player" by default, but you can modify the code to allow dynamic player names if desired.

## License
This project is licensed under the MIT License - see the LICENSE file for details.



### Features of the `README.md`:
- **Game Description**: Brief explanation of the game and its mechanics.
- **Installation Instructions**: Steps to install Pygame and run the game.
- **How to Play**: Instructions on controlling the game.
- **Database Info**: Details about the SQLite database used to store scores.
- **License Section**: You can update this with your license details (e.g., MIT License).

Feel free to update the repository URL in the "Clone the Repository" section and adjust any 