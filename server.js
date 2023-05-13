const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const bodyParser = require('body-parser');
const path = require('path');
const crypto = require('crypto');
/* importing libraries */

// Creates application in Express
const app = express();
// Middleware that helpd parse URLencoded bodies
app.use(bodyParser.urlencoded({ extended: true }));

// using EJS as the html templating engine
app.set('view engine', 'ejs');

// Create a HTTP and Websocket server
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// connecting to MongoDB
mongoose.connect('mongodb://mongo:27017/mydb', {useNewUrlParser: true, useUnifiedTopology: true});

// Creating a Schema
const SchemaForUser = new mongoose.Schema({
  username: String,
  password: String,
  salt: String,
  wins: { type: Number, default: 0 }
});

// Create a Model
const User = mongoose.model('User', SchemaForUser);

// variable to store the games
let games = {};

// HomePage
app.get('/', (req, res) => {
    const fileName = 'index.html';
    const filePath = path.join(__dirname, 'public', fileName);
    res.sendFile(filePath);
});

// HomePage
app.get('/index.html', (req, res) => {
  const fileName = 'index.html';
  const filePath = path.join(__dirname, 'public', fileName);
  res.sendFile(filePath);
});

// Register Page
app.get('/register.html', (req, res) => {
    const fileName = 'register.html';
    const filePath = path.join(__dirname, 'public', fileName);
    res.sendFile(filePath);
});

// Landing Page *MIGHT REMOVE*
app.get('/LandingPage.html', (req, res) => {
    const fileName = 'LandingPage.html';
    const filePath = path.join(__dirname, 'public', fileName);
    res.sendFile(filePath);
});

// Send Client Side JavaScript
app.get('/public/client.js', (req, res) => {
    const fileName = 'client.js';
    const filePath = path.join(__dirname, 'public', fileName);
    res.sendFile(filePath);
});

// When Client submits the form
app.post('/register', async (req, res) => {
  try {
    // Check if password and confirm password fields match
    if (req.body.password !== req.body['confirm-password']) {
      return res.status(400).send('Passwords do not match');
    }

    const salt = await bcrypt.genSalt();
    const hashedPassword = await bcrypt.hash(req.body.password, salt);

    const user = new User({
      username: req.body.username,
      email: req.body.email, // store email
      password: hashedPassword,
      salt: salt
    });

    const result = await user.save();
    res.redirect('/'); // Redirect to the root path

  } catch (error) {
    res.status(500).send(error);
  }
});

// Get the number of wins and highest go at top
app.get('/leaderboard', async (req, res) => {
  try {
      const users = await User.find().sort({ wins: -1 }).limit(10);
      res.json(users);
  } catch (error) {
      res.status(500).send(error);
  }
});

// Display Leaderboard
app.get('/leaderboard.html', (req, res) => {
  const fileName = 'leaderboard.html';
  const filePath = path.join(__dirname, 'public', fileName);
  res.sendFile(filePath);
});

// When client submits the login form
app.post('/login', async (req, res) => {
    try {
        const user = await User.findOne({ username: req.body.username });
        if (!user) {
            return res.status(400).send({ message: 'User not found' });
        }

        const validPassword = await bcrypt.compare(req.body.password, user.password);
        if (!validPassword) {
            return res.status(400).send({ message: 'Invalid password' });
        }

        const token = crypto.randomBytes(32).toString('hex');
        const hashedToken = await bcrypt.hash(token, 10);

        //user.hashedToken = hashedToken;
        //await user.save();

        res.render('LandingPage', { username: user.username });

    } catch (error) {
        res.status(500).send(error);
    }
});

// Handles websocket messages and updates state of the game
wss.on('connection', (ws) => {
  ws.on('message', async (message) => {
    const data = JSON.parse(message);
    switch (data.type) {
      case 'create':
        let gameId = uuidv4();
        games[gameId] = {
          id: gameId,
          players: [ws],
          board: Array(9).fill(null),
          currentPlayer: 0,
        };
        ws.send(JSON.stringify({ type: 'created', gameId: gameId }));
        break;
      case 'join':
        let game = games[data.gameId];
        if (game && game.players.length < 2) {
          game.players.push(ws);
          game.players.forEach((player, index) => {
            player.send(
              JSON.stringify({
                type: 'start',
                player: index,
                board: game.board,
                currentPlayer: game.currentPlayer,
              })
            );
          });
        } else {
          ws.send(JSON.stringify({ type: 'error', message: 'Cannot join game' }));
        }
        break;
      case 'move':
        let currentGame = games[data.gameId];
        if (currentGame && currentGame.board[data.index] === null && currentGame.currentPlayer === data.player) {
          currentGame.board[data.index] = data.player;
          currentGame.currentPlayer = (currentGame.currentPlayer + 1) % 2;
        
          // Check for a winner
          const winner = checkWin(currentGame.board);
          let gameEndMessage;
        
          if (winner !== null) {
            gameEndMessage = { type: 'end', message: `Player ${winner} wins!` };
            // Update winner in DB
            try {
              console.log(User.findOne({ username: data.username }));
              await User.findOneAndUpdate(
                { username: data.username }, 
                { $inc: { wins: 1 } },
                { new: true }
              );
            } catch (err) {
              console.log(err);
            }
          } else if (!currentGame.board.includes(null)) { // Check for a draw
            gameEndMessage = { type: 'end', message: 'Draw!' };
          }
        
          currentGame.players.forEach((player) => {
            player.send(JSON.stringify({
              type: 'move',
              board: currentGame.board,
              currentPlayer: currentGame.currentPlayer,
            }));
        
            if (gameEndMessage) {
              player.send(JSON.stringify(gameEndMessage));
            }
          });
        }
        break;
        
    }
  });

  ws.on('close', () => {
    for (let gameId in games) {
      let game = games[gameId];
      let playerIndex = game.players.indexOf(ws);
      if (playerIndex !== -1) {
        game.players.splice(playerIndex, 1);
        if (game.players.length === 0) {
          delete games[gameId];
        }
      }
    }
  });
});

// Check if a player has won a game
function checkWin(board) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];

  for (let line of lines) {
    const [a, b, c] = line;
    if (board[a] !== null && board[a] === board[b] && board[a] === board[c]) {
      return board[a];
    }
  }

  return null;
}

server.listen(8080, () => {
  console.log('Server started on port 8080');
});
