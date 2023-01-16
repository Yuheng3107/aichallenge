
function getFeedback() {
    socket.emit('feedback');
}

const startButton = document.querySelector('.start-button');
const endButton = document.querySelector('.end-button');
const repCount = document.querySelector('#rep-count');
const repFeedback = document.querySelector("#rep-feedback");
const feedback = document.querySelector('#feedback');
const form = document.querySelector('#changeExercise');
const showLogButton = document.querySelector("#show-log-button");
const feedbackList = document.querySelector('#feedback-list');
const summary = document.querySelector('#summary');
const textToSpeechButton = document.querySelector('.text-to-speech');



let synth;
let textToSpeech = false;


if ('speechSynthesis' in window) {
    synth = window.speechSynthesis;
    textToSpeech = true;
}
else {
    // replace with overlay and div pop-up in the future
    alert('text to speech not available');

}
let started = false;
let socket = io();

startButton.addEventListener('click', (e) => {
    // runs python script that starts Peekingduck
    if (!started) {
        fetch(startButton.getAttribute('data-url'));
        startButton.style.display = "none";
        started = true;

        // updates feedback every second
        setInterval(getFeedback, 200);
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
socket.on('feedback', (stringData) => {
    let data = JSON.parse(stringData);
    // if repCount changes, update text display on screen
    if (Number(repCount.textContent) != data["repCount"]) {
        repFeedback.textContent = data.repFeedback.slice(-1);
        //append list items to the feedback log
        console.log(data);
        let li = document.createElement('li');
        li.innerText = data.repFeedback.slice(-1);
        feedbackList.insertBefore(li, feedbackList.firstChild);

        if (textToSpeech) {
            // if text to speech available, speak most recent rep 
            let speech = new SpeechSynthesisUtterance(feedbackList.firstChild.innerText);
            synth.speak(speech);
        }
    }
    repCount.textContent = data["repCount"];
    summary.innerText = data.summary;

})

showLogButton.addEventListener('click', (event) => {
    showLogButton.classList.toggle('active');
    feedbacklist.classList.toggle('active');
})



textToSpeechButton.addEventListener('click', () => {
    if (textToSpeech) {
        textToSpeech = false;
        textToSpeechButton.classList.remove('btn-danger');
        textToSpeechButton.classList.add('btn-success');
        textToSpeechButton.innerText = "Turn On Text-To-Speech";
    }
    else {
        textToSpeech = true;
        textToSpeechButton.classList.remove('btn-success');
        textToSpeechButton.classList.add('btn-danger');
        textToSpeechButton.innerText = "Turn Off Text-To-Speech";
    }
})


