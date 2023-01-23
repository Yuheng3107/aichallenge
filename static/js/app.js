
function getFeedback() {
    socket.emit('feedback');
}

function getVideoFrames() {
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    let dataURL = canvas.toDataURL('image/jpeg');
    console.log(dataURL);
    socket.emit('video', {'url': dataURL});
}
const startButton = document.querySelector('.start-button');
const endButton = document.querySelector('.end-button');
const repInfo = document.querySelector('rep-info-group');
const repCount = document.querySelector('#rep-count');
const repFeedback = document.querySelector("#rep-feedback");
const feedback = document.querySelector('#feedback');
const form = document.querySelector('#changeExercise');
const showLogButton = document.querySelector("#show-log-button");
const feedbackList = document.querySelector('#feedback-list');
const summary = document.querySelector('#summary');
const textToSpeechButton = document.querySelector('.text-to-speech');
const stressFeedback = document.querySelector('#stress-feedback');
const difficultyButton = document.querySelector('#difficulty');
const video = document.querySelector("#video");
const canvas = document.querySelector("#canvas");

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

document.addEventListener('DOMContentLoaded', (event) => {

    // is this even
    if (!repCount.textContent) {
        repCount.style.display = 'none';
    }
    if (!repFeedback.textContent) {
        repFeedback.style.display = 'none';
    }
})

startButton.addEventListener('click', (e) => {
    
    if (!started) {
        // runs python script that starts Peekingduck if PeekingDuck is not already running
        socket.emit('start');

        startButton.style.display = "none";
        started = true; 

        if ('mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices) {
            // checks that browser supports getting camera feed from user
            // if so use the getUserMedia API to get video from the user, after
            // asking for permission from the user


            navigator.mediaDevices.getUserMedia({ video: true}).then(function(stream) {
                video.srcObject = stream;
                setInterval(getVideoFrames, 50);
            }).catch(function(err) {
                console.log("An error occurred: " + err);
            });
          }
        

        // updates feedback every second
        // setInterval(getFeedback, 200);
    }
});
endButton.addEventListener('click', () => {
    socket.emit('endExercise');
});

form.addEventListener('submit', (e) => {
    // prevents default form submission 
    e.preventDefault();
    let exerciseId = form.elements["exerciseId"].value;
    // calls python function to update exercise id
    socket.emit('changeExercise', exerciseId);
    // Make repCount and repFeedback visible
    repCount.style.display = 'flex';
    repFeedback.style.display = 'flex';
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
    stressFeedback.innerText = data.stressFeedback;

})

showLogButton.addEventListener('click', (event) => {
    showLogButton.classList.toggle('active');
    feedbackList.classList.toggle('active');
    if (showLogButton.classList.contains("active")) {
        showLogButton.children.childNodes[0].textContent = "Hide Feedback Log";
    } else {
        showLogButton.children.childNodes[0].textContent = "Show Feedback Log";
    }
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


difficultyButton.addEventListener('click', () => {
    console.log('Test');
    if (difficultyButton.classList.contains('btn-danger')) {
        difficultyButton.innerText = 'Beginner';
        socket.emit('changeDifficulty', 'Beginner');
    }
    else {
        difficultyButton.innerText = 'Expert';
        socket.emit('changeDifficulty', 'Expert');
    }
    difficultyButton.classList.toggle('btn-danger');
    difficultyButton.classList.toggle('btn-success');
})




