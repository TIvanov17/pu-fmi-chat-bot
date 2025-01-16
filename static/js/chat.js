// Connect to the Flask-SocketIO server
const socket = io.connect(window.location.origin);

socket.on('connected', function(data) {
    appendMessage('Bot: ' + data.message, 'bot');
});

// Function to send user input to the server
function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    // Append user message to the chatbox
    appendMessage('You: ' + userInput, 'user');

    // Send message to the server
    socket.emit('user_message', userInput);

    // Clear the input box
    document.getElementById('user-input').value = '';
}

// Function to append messages to the chatbox
function appendMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add(sender);
    messageDiv.textContent = message;
    messageDiv.innerHTML = message.replace(/\n/g, '<br>');
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to bottom
}

function clearChat() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';
}
// Listen for the chatbot response
socket.on('bot_reply', function(response) {
    appendMessage('Bot: ' + response, 'bot');
});
