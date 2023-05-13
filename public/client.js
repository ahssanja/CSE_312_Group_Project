// Creating a Websocket connection
const ws = new WebSocket('wss://final312project.games/');

let player;
let gameBoard;
let gameId;
let currentPlayer = null;
let gameInfo = document.querySelector('#game-info');

// What to run when Websocket is open
ws.onopen = () => {
  ws.send(JSON.stringify({ type: 'create' }));
};

// What to do when Websocket recieves messages
ws.onmessage = (event) => {
  let data = JSON.parse(event.data);
  switch (data.type) {
    case 'created':
      gameId = data.gameId;
      gameInfo.textContent = 'Game created with ID: ' + gameId;
      break;
    case 'start':
      player = data.player;
      gameBoard = data.board;
      currentPlayer = data.currentPlayer;
      gameInfo.textContent = 'Game started. You are player: ' + player;
      renderBoard();
      break;
    case 'move':
      gameBoard = data.board;
      currentPlayer = data.currentPlayer;
      renderBoard();
      break;
    case 'end':
      gameInfo.textContent = data.message; // Winning Message
      setTimeout(() => { // Add a pause
        window.location.href = '/leaderboard.html'; // Redirect to the leaderboard
      }, 3000); // 3 sec
      break;
    case 'error':
      console.error('Error: ' + data.message);
      break;
  }
};

// Keeps and Updates the board/state of the baord
function renderBoard() {
    let cells = document.querySelectorAll('.cell');
    cells.forEach((cell, index) => {
        cell.textContent = gameBoard[index] !== null ? (gameBoard[index] === 0 ? 'X' : 'O') : '';
        cell.addEventListener('click', () => {
        if (gameBoard[index] === null && currentPlayer === player) {
            ws.send(JSON.stringify({ type: 'move', index: index, player: player, gameId: gameId, username: username }));
        }
        });
    });
}

// listens for when button is pressed and generates a random id
document.querySelector('#join-btn').addEventListener('click', () => {
  let input = document.querySelector('#join-input');
  gameId = input.value;
  if (gameId) {
    ws.send(JSON.stringify({ type: 'join', gameId: gameId }));
  }
});
