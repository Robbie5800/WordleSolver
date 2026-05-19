let guessCount = 1;
// Global array to track past turns across submissions
let guessHistory = [];

function addCourse() {
    // find main board
    const container = document.getElementById('game-board');
    if (!container) return;

    guessCount++; // increment the guess counter
    
    const newRow = document.createElement('div');
    newRow.className = 'row added-row'; 
    
    newRow.innerHTML = `
        <p class="guess-title">Guess ${guessCount}:</p>
        <div class="letters">
            <!-- Letter 1 -->
            <div class="input-container">
                <button class="green-button"></button>
                <button class="yellow-button"></button>
                <button class="grey-button"></button>
                <input type="text" class="square-letter" maxlength="1" placeholder="">
            </div>
            <!-- Letter 2 -->
            <div class="input-container">
                <button class="green-button"></button>
                <button class="yellow-button"></button>
                <button class="grey-button"></button>
                <input type="text" class="square-letter" maxlength="1" placeholder="">
            </div>
            <!-- Letter 3 -->
            <div class="input-container">
                <button class="green-button"></button>
                <button class="yellow-button"></button>
                <button class="grey-button"></button>
                <input type="text" class="square-letter" maxlength="1" placeholder="">
            </div>
            <!-- Letter 4 -->
            <div class="input-container">
                <button class="green-button"></button>
                <button class="yellow-button"></button>
                <button class="grey-button"></button>
                <input type="text" class="square-letter" maxlength="1" placeholder="">
            </div>
            <!-- Letter 5 -->
            <div class="input-container">
                <button class="green-button"></button>
                <button class="yellow-button"></button>
                <button class="grey-button"></button>
                <input type="text" class="square-letter" maxlength="1" placeholder="">
            </div>
        </div>
    `;
    
    container.appendChild(newRow);
}

// Wait for the DOM to fully load
document.addEventListener('DOMContentLoaded', () => {
    const gameBoard = document.getElementById('game-board');

    if (gameBoard) {
        // Listen for clicks inside the entire game board
        gameBoard.addEventListener('click', (event) => {
            const target = event.target;

            // check for color button press
            if (target.classList.contains('green-button') || 
                target.classList.contains('yellow-button') || 
                target.classList.contains('grey-button')) {
                
                // select the correct row
                const container = target.closest('.input-container');
                if (!container) return;

                // use correct letter
                const inputSquare = container.querySelector('.square-letter');
                if (!inputSquare) return;

                // change letter color to white && change background to selected color
                let newBgColor = '';
                let newTextColor = '#ffffff';

                if (target.classList.contains('green-button')) {
                    newBgColor = '#6aaa64'; // Wordle Green
                } else if (target.classList.contains('yellow-button')) {
                    newBgColor = '#c9b458'; // Wordle Yellow
                } else if (target.classList.contains('grey-button')) {
                    newBgColor = '#787c7e'; // Wordle Grey
                }

                // update new preferences for text and bg color
                inputSquare.style.backgroundColor = newBgColor;
                inputSquare.style.color = newTextColor;
                inputSquare.style.borderColor = newBgColor; 
            }
        });
    }
});

function getCompressedRowData() {
    // grab current row
    const rows = document.querySelectorAll('#game-board .row');
    const latestRow = rows[rows.length - 1];
    if (!latestRow) return null;

    const letterContainers = latestRow.querySelectorAll('.input-container');
    
    let wordString = "";
    let colorPatternString = "";
    let hasValidationErrors = false;

    // build word from front end
    letterContainers.forEach((container) => {
        const input = container.querySelector('.square-letter');
        const letter = input.value.trim().toLowerCase(); // Normalize letter input
        const bgColor = input.style.backgroundColor;

        // input val
        if (!letter) {
            hasValidationErrors = true;
        }
        wordString += letter;

        // switch to input for python "gxy"
        if (bgColor === 'rgb(106, 170, 100)' || bgColor === '#6aaa64') {
            colorPatternString += 'g'; // Green
        } else if (bgColor === 'rgb(201, 180, 88)' || bgColor === '#c9b458') {
            colorPatternString += 'y'; // Yellow
        } else if (bgColor === 'rgb(120, 124, 126)' || bgColor === '#787c7e') {
            colorPatternString += 'x'; // Absent
        } else {
            // No color button was clicked for this tile
            hasValidationErrors = true; 
        }
    });

    if (hasValidationErrors) {
        alert("Please make sure all 5 boxes have a letter and an assigned color status!");
        return null;
    }

    // Return the clean data structure expected by your backend
    return {
        words: wordString,          // e.g., "words"
        pattern: colorPatternString // e.g., "ggyxg"
    };
}

function submitGuess() {
    const formattedPayload = getCompressedRowData();
    if (!formattedPayload) return; // Halt if validation failed

    // Package BOTH the current turn data and the previous history list
    const outboundData = {
        words: formattedPayload.words,
        pattern: formattedPayload.pattern,
        history: guessHistory 
    };

    console.log("Sending compressed data to Python:", outboundData);

    // Send the cleanly formatted payload to Python
    fetch('submit-guess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(outboundData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success response from Python:', data);
        
        // Push current round metadata into history array after successful calculation
        guessHistory.push(formattedPayload);

        // Update the HTML text elements with the recommendations from Python
        if (data.recommendations && data.recommendations.length >= 3) {
            document.getElementById('rec-1').innerText = data.recommendations[0];
            document.getElementById('rec-2').innerText = data.recommendations[1];
            document.getElementById('rec-3').innerText = data.recommendations[2];
        }
        
        // Update the remaining possible words counter
        if (data.remaining_count !== undefined) {
            document.getElementById('remaining-count').innerText = `Possible words remaining: ${data.remaining_count}`;
        }

        // Automatically build the next guess line for the user
        addCourse(); 
    })
    .catch((error) => {
        console.error('Network Error:', error);
    });
}

