function printBoard(board) {
  console.log("-------------");
  for (let i = 0; i < 3; i++) {
    process.stdout.write("| ");
    for (let j = 0; j < 3; j++) {
      process.stdout.write(board[i][j] + " | ");
    }
    console.log("");
    console.log("-------------");
  }
}

function checkWinner(board) {
  for (let i = 0; i < 3; i++) {
    if (board[i][0] === board[i][1] && board[i][1] === board[i][2] && board[i][0] !== " ") {
      return board[i][0];
    } else if (board[0][i] === board[1][i] && board[1][i] === board[2][i] && board[0][i] !== " ") {
      return board[0][i];
    }
  }
  if (board[0][0] === board[1][1] && board[1][1] === board[2][2] && board[0][0] !== " ") {
    return board[0][0];
  } else if (board[0][2] === board[1][1] && board[1][1] === board[2][0] && board[0][2] !== " ") {
    return board[0][2];
  }
  return null;
}

function ticTacToe() {
  let board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]];
  let player = "X";
  let winner = null;

  while (winner == null) {
    printBoard(board);
    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });
    readline.question(`Enter row (1-3) for player ${player}: `, (row) => {
      readline.question(`Enter column (1-3) for player ${player}: `, (col) => {
        row = parseInt(row) - 1;
        col = parseInt(col) - 1;
        if (board[row][col] === " ") {
          board[row][col] = player;
          if (player === "X") {
            player = "O";
          } else {
            player = "X";
          }
          winner = checkWinner(board);
        }
        readline.close();
      });
    });
  }
  printBoard(board);
  console.log(`Player ${winner} wins!`);
}
