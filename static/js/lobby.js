let socket = io();
let appSocket = io('/app');
const sendButton = document.querySelector('#sendButton');
const myMessage = document.querySelector('#myMessage');
const messages = document.querySelector('#messages');
const alerter = document.querySelector('#alerter');
const clearChatButton = document.querySelector('#clearChatButton');

const alert = (message, type) => {
    alerter.innerHTML = [
      `<div class="alert alert-${type} alert-dismissible mt-3" role="alert">`,
      `   <div>${message}</div>`,
      '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
      '</div>'
    ].join('')
}

socket.on('connect', () => {
    socket.send('User has connected');
});

// sends text in input to backend, and backend will send to all clients
sendButton.addEventListener('click', (e) => {
    socket.send(myMessage.value);
});

myMessage.addEventListener('keypress', (e) => {
    if (e.key === "Enter") {
        sendButton.click();
    }
});

socket.on('message', (msg) => {
    let li = document.createElement('li');
    li.innerText = msg;
    messages.insertBefore(li, messages.firstChild);
});

appSocket.on('peekingduckFree', () => {
    alert('Application is now free to use.','success');
})

function resetServer() {
    socket.emit('resetServer');
}

clearChatButton.addEventListener('click', () => {
    messages.innerHTML = '';
})