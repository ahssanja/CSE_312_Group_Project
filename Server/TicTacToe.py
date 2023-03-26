def print_board(board):
    print("-------------")
    for i in range(3):
        print("|", end=" ")
        for j in range(3):
            print(board[i][j], "|", end=" ")
        print()
        print("-------------")

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        elif board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

def tic_tac_toe():
    board = [[" ", " ", " "],
             [" ", " ", " "],
             [" ", " ", " "]]
    player = "X"
    winner = None

    while winner is None:
        print_board(board)
        row = int(input("Enter row (1-3) for player " + player + ": ")) - 1
        col = int(input("Enter column (1-3) for player " + player + ": ")) - 1
        if board[row][col] == " ":
            board[row][col] = player
            if player == "X":
                player = "O"
            else:
                player = "X"
            winner = check_winner(board)

    print_board(board)
    print("Player", winner, "wins!")

tic_tac_toe()

