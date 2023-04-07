const board = ['', '', '', '', '', '', '', '', ''];
let player = 'X';
let gameOver = false;

function playerTurn(index) {
    if (!gameOver && board[index] === '') {
        board[index] = player;
        
        //swap player

        document.getElementById('cell' + index).className = player;
        document.getElementById('cell' + index).innerHTML = player;
        checkWinner();

        if (player === 'O') {
            player = 'X';
          } 
        else{
            player = 'O';
        }
    }
}


function checkWinner() {
    const allcombinations = [
        [0, 1, 2], //first row
        [3, 4, 5], //second row
        [6, 7, 8], // third row
        [0, 3, 6], //first column
        [1, 4, 7], //second column
        [2, 5, 8], //third column
        [0, 4, 8], //l-r diagona
        [2, 4, 6] // r-l diagonal
    ];

    const arraylen = allcombinations.length

    for (let i = 0; i < arraylen; i++) {

        // check through all 3 digits of each array 
        let first = allcombinations[i][0];
        let second = allcombinations[i][1];
        let third = allcombinations[i][2];

        if (board[first] !== '' && board[second] !== '' && board[third] !== '' ){
            if (board[first] === board[second] && board[first] === board[third] && board[second] === board[third]){
                document.getElementById('message').innerHTML = board[first] + ' wins!';
            gameOver = true;
            break;
            }
        }

    }

    if (!gameOver && board.indexOf('') === -1) {  //all tiles are full
        document.getElementById('message').innerHTML = 'Tie game!';
        gameOver = true;
    }

}

document.getElementById("lobby").addEventListener("click", function(){
    var intervalId = setInterval(checkForPlayer, 10000);
    fetch("/lookingforplayers", {method: "POST"}).then(response =>{
        if (response.ok){

            return intervalId

        }
    });

    function checkForPlayer() {
        fetch("/checklobby", {method: "GET"}).then(response =>{
            if (response.ok) {
                response.json().then(json_data => {
                    if (json_data.length === 2) {
                        clearInterval(intervalId);
                        window.location.href = "../HTML/Game.html";
                    }
                });
            }
        });
    }
});







