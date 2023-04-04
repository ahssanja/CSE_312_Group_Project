var board = ['', '', '', '', '', '', '', '', ''];
var player = 'X';
var gameOver = false;

function playTurn(index) {
    if (!gameOver && board[index] === '') {
        board[index] = player;
        document.getElementById('cell-' + index).className = player;
        document.getElementById('cell-' + index).innerHTML = player;
        checkWinner();
        player = player === 'X' ? 'O' : 'X';
    }
}

function checkWinner() {
    var winningCombinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ];

    for (var i = 0; i < 8; i++) {
        var a = winningCombinations[i][0];
        var b = winningCombinations[i][1];
        var c = winningCombinations[i][2];

        if (board[a] !== '' && board[a] === board[b] && board[b] === board[c]) {
            document.getElementById('message').innerHTML = board[a] + ' wins!';
            gameOver = true;
            break;
        }
    }

    if (!gameOver && board.indexOf('') === -1) {
        document.getElementById('message').innerHTML = 'Tie game!';
        gameOver = true;
    }
}


// function printBoard(board) {
//   console.log("-------------");
//   for (let i = 0; i < 3; i++) {
//     process.stdout.write("| ");
//     for (let j = 0; j < 3; j++) {
//       process.stdout.write(board[i][j] + " | ");
//     }
//     console.log("");
//     console.log("-------------");
//   }
// }
//
// function checkWinner(board) {
//   for (let i = 0; i < 3; i++) {
//     if (board[i][0] === board[i][1] && board[i][1] === board[i][2] && board[i][0] !== " ") {
//       return board[i][0];
//     } else if (board[0][i] === board[1][i] && board[1][i] === board[2][i] && board[0][i] !== " ") {
//       return board[0][i];
//     }
//   }
//   if (board[0][0] === board[1][1] && board[1][1] === board[2][2] && board[0][0] !== " ") {
//     return board[0][0];
//   } else if (board[0][2] === board[1][1] && board[1][1] === board[2][0] && board[0][2] !== " ") {
//     return board[0][2];
//   }
//   return null;
// }
//
// function ticTacToe() {
//   let board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]];
//   let player = "X";
//   let winner = null;
//
//   while (winner == null) {
//     printBoard(board);
//     const readline = require('readline').createInterface({
//       input: process.stdin,
//       output: process.stdout
//     });
//     readline.question(`Enter row (1-3) for player ${player}: `, (row) => {
//       readline.question(`Enter column (1-3) for player ${player}: `, (col) => {
//         row = parseInt(row) - 1;
//         col = parseInt(col) - 1;
//         if (board[row][col] === " ") {
//           board[row][col] = player;
//           if (player === "X") {
//             player = "O";
//           } else {
//             player = "X";
//           }
//           winner = checkWinner(board);
//         }
//         readline.close();
//       });
//     });
//   }
//   printBoard(board);
//   console.log(`Player ${winner} wins!`);
// }
//


