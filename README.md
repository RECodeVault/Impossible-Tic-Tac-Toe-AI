# Unbeatable Tic Tac Toe AI (With explanation)

This project presents an unbeatable Tic Tac Toe AI implementation utilizing the powerful Minimax algorithm. Tic Tac Toe, also known as Noughts and Crosses, is a classic game that involves two players alternately placing their marks (X or O) on a 3x3 grid. The objective is to be the first to form a horizontal, vertical, or diagonal line of three marks.

## How to Install

1. **Clone the repository:**
    ```bash
    git clone https://github.com/RECodeVault/Impossible-Tic-Tac-Toe-AI.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd Impossible-Tic-Tac-Toe-AI
    ```

3. **Install dependencies:**
    ```bash
    pip3 install -r requirements.txt
    ```

4. **Start the application:**
    ```bash
    python runner.py
    ```

## Example of running program:
![Running program](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWN6ZzE4dmxxYTdtamhoZDA5eThzNnRxbjh0eGo4bGI5ZTg2a25jdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6FaLCPjL2Dj93cb96t/giphy.gif)

## Explanation of Minimax Algorithm

### Recursive Evaluation:

The algorithm starts by considering the current state of the game and recursively evaluates all possible future moves.
At each level of recursion, it alternates between players, simulating each player's turn.

### Evaluation Function:

At the terminal states (i.e., when the game ends), the algorithm evaluates the game state using an evaluation function.
This evaluation function assigns a score to the state, representing how favorable it is for the current player.

### Backpropagation:

As the recursion unwinds, the algorithm propagates the scores back up the tree.
For each level, if it's the maximizing player's turn, it chooses the move with the highest score, assuming the opponent will also make the best moves.
If it's the minimizing player's turn, it chooses the move with the lowest score, assuming the opponent will try to maximize their own score.

### Decision Making:

Once the entire tree is evaluated, the algorithm selects the move that leads to the best possible outcome for the current player.
This move is the one with the highest score at the root level of the tree.

### Example Diagram

![Minimax Algorithm Diagram](https://alialaa.com/static/38d8b0523fa99f139df7564e6def9a61/c58a3/minimax.jpg)

In this diagram, you can see the decision tree for a simple game. Each node represents a possible game state, and the edges represent possible moves. The Minimax algorithm evaluates each node to determine the best move for the current player.
