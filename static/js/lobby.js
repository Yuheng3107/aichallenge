let socket = io();
const sendButton = document.querySelector('#sendButton');
const myMessage = document.querySelector('#myMessage');
const messages = document.querySelector('#messages');

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
})

socket.on('message', (msg) => {
    let li = document.createElement('li');
    li.innerText = msg;
    messages.appendChild(li);
});