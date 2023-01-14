
function getFeedback() {
    socket.emit('feedback');
}

const startButton = document.querySelector('.start-button');
const endButton = document.querySelector('.end-button');
const repCount = document.querySelector('#rep-count');
const feedback = document.querySelector('#feedback');
const form = document.querySelector('#changeExercise');

let started = false;
let socket = io();

startButton.addEventListener('click', (e) => {
    // runs python script that starts Peekingduck
    if (!started) {
        fetch(startButton.getAttribute('data-url'));
        startButton.style.display = "none";
        started = true;
        
        // updates feedback every second
        setInterval(getFeedback, 1000);
    }
});
endButton.addEventListener('click', () => {
    fetch(endButton.getAttribute('data-url'));
});

form.addEventListener('submit', (e) => {
    // prevents default form submission 
    e.preventDefault();
    let exerciseId = form.elements["exerciseId"].value;
    // calls python function to update exercise id
    socket.emit('changeExercise', exerciseId);
});

// Listens for feedback event from server which updates
// front end 
socket.on('feedback', data => {
    console.log(data);
    repCount.textContent = data[0];
    feedback.textContent = data.slice(1);
})




