import math

class TicTacToe:
    def __init__(self):
        # Create an empty 3x3 board
        self.board = [" " for _ in range(9)]
        self.current_winner = None  # Tracks the winner of the game

    def print_board(self):
        # Print the board in a readable format
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    @staticmethod
    def print_board_indices():
        # Print board positions for user reference
        print("\nBoard Positions:")
        for row in [[i * 3 + j for j in range(3)] for i in range(3)]:
            print("| " + " | ".join(map(str, row)) + " |")

    def available_moves(self):
        # Returns a list of available moves
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def empty_squares(self):
        # Check if there are any empty squares left
        return " " in self.board

    def num_empty_squares(self):
        # Count the number of empty squares
        return self.board.count(" ")

    def make_move(self, square, letter):
        # Make a move if the square is valid
        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):  # Check if this move wins the game
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check if there's a winner in the row, column, or diagonals
        row_index = square // 3
        row = self.board[row_index * 3:(row_index + 1) * 3]
        if all([s == letter for s in row]):
            return True

        col_index = square % 3
        column = [self.board[col_index + i * 3] for i in range(3)]
        if all([s == letter for s in column]):
            return True

        if square % 2 == 0:  # Check diagonals (only for even squares)
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal1]) or all([s == letter for s in diagonal2]):
                return True

        return False


def minimax(game, depth, maximizing_player):
    # Base case: Check if the game is over and return a score
    if game.current_winner == "O":  # AI wins
        return {"position": None, "score": 10 - depth}
    elif game.current_winner == "X":  # Human wins
        return {"position": None, "score": depth - 10}
    elif not game.empty_squares():  # Tie
        return {"position": None, "score": 0}

    if maximizing_player:  # AI's turn
        best = {"position": None, "score": -math.inf}
        for move in game.available_moves():
            game.make_move(move, "O")
            sim_score = minimax(game, depth + 1, False)  # Recursively evaluate moves
            game.board[move] = " "  # Undo move
            game.current_winner = None  # Reset winner
            sim_score["position"] = move
            if sim_score["score"] > best["score"]:
                best = sim_score
        return best
    else:  # Human's turn
        best = {"position": None, "score": math.inf}
        for move in game.available_moves():
            game.make_move(move, "X")
            sim_score = minimax(game, depth + 1, True)  # Recursively evaluate moves
            game.board[move] = " "  # Undo move
            game.current_winner = None  # Reset winner
            sim_score["position"] = move
            if sim_score["score"] < best["score"]:
                best = sim_score
        return best


def play_game():
    print("Welcome to Tic Tac Toe!")
    game = TicTacToe()
    TicTacToe.print_board_indices()

    human_letter = "X"  # Human always plays as X
    ai_letter = "O"     # AI plays as O

    while game.empty_squares():
        # Human's turn
        if game.num_empty_squares() > 0 and not game.current_winner:
            move = None
            while move not in game.available_moves():
                try:
                    move = int(input("\nYour Turn (X). Enter position (0-8): "))
                except ValueError:
                    print("Invalid input. Try again.")
            game.make_move(move, human_letter)
            print("\nYour Move:")
            game.print_board()

        # Check for game over
        if game.current_winner:
            print("\nCongratulations! You win!" if game.current_winner == human_letter else "\nAI wins!")
            break
        elif not game.empty_squares():
            print("\nIt's a tie!")
            break

        # AI's turn
        if game.num_empty_squares() > 0 and not game.current_winner:
            print("\nAI's Turn (O):")
            ai_move = minimax(game, 0, True)["position"]  # AI chooses the best move
            game.make_move(ai_move, ai_letter)
            game.print_board()

        # Check for game over again
        if game.current_winner:
            print("\nCongratulations! You win!" if game.current_winner == human_letter else "\nAI wins!")
            break
        elif not game.empty_squares():
            print("\nIt's a tie!")
            break


if __name__ == "__main__":
    play_game()
