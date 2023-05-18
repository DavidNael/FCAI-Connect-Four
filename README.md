# Connect Four Game

Welcome to the Connect Four game repository! This project is a Python implementation of the classic Connect Four game, which includes an AI component for an enhanced gaming experience. Connect Four is a two-player strategy game where the objective is to connect a line of four discs of your color vertically, horizontally, or diagonally before your opponent does.

## Features

- **Three Game Modes**
  - **2 Player Mode**: Play against a friend locally. Take turns dropping discs and compete to be the first to connect four in a row.
  - **Player vs AI Mode**: Challenge yourself against an AI opponent. Test your strategic skills and try to outsmart the computer.
  - **AI vs AI Mode**: Sit back and watch two AI opponents battle it out. Observe different strategies as the AI players compete to win.

- **Intelligent AI**: The AI player utilizes the minmax algorithm to make intelligent moves. It analyzes the game board and predicts the best possible moves to maximize its chances of winning.

- **Interactive Interface**: The game provides a user-friendly interface. The board is displayed visually, and the players can easily select their moves by clicking on the desired column.

## Getting Started


### Prerequisites

To run the Connect Four game, you need to have Python 3.x installed on your machine. Additionally, the project relies on the following external libraries:

- `random`: for generating random moves during AI gameplay.
- `numpy`: for efficient array operations and board manipulation.
- `pygame`: for creating the game interface and handling graphics.
- `sys`: for system-related functionality, such as exiting the game.
- `math`: for mathematical operations used in the game logic.
- `time`: for introducing delays between moves and adding animations.

You can install these dependencies using the following command:

```
pip install numpy pygame
```

Please make sure to have Python 3.x installed, and then you can proceed with the installation and usage instructions mentioned in the previous README.

### Installation

1. Clone this repository to your local machine using the following command:

```
git clone https://github.com/DavidNael/FCAI-Connect-Four.git
```

2. Navigate to the project directory:

```
cd connect-four
```

### Usage

To start the Connect Four game, simply run the `connect_four.py` script:

```
python connect_four.py
```

Follow the on-screen instructions to select the game mode and begin playing.

## Acknowledgements

- The Connect Four game logic and AI algorithms were inspired by various resources and tutorials available online.
