
function getFeedback() {
    socket.emit('feedback');
}

const startButton = document.querySelector('.start-button');
const endButton = document.querySelector('.end-button');
const repInfo = document.querySelector('#rep-info-group');
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
const camPosition = document.querySelector("#cam-position");
const toggleContainer = document.querySelector(".toggle-container")  

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
    //hide the repcount and repfeedback on page load since there's no content
    
    if (!repCount.textContent) {
        repCount.style.display = 'none';
    }
    if (!repFeedback.textContent) {
        repFeedback.style.display = 'none';
    }
})

startButton.addEventListener('click', (e) => {
    console.log('start button clicked');
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
    socket.emit('endExercise');
    summary.classList.add("w-50", "fs-4", "card", "p-3", "mt-3");
    repInfo.style.display='none';
    console.log('end button clicked');
});

const alert = (message, type) => {
    const wrapper = document.createElement('div')
    wrapper.innerHTML = [
      `<div class="alert alert-${type} alert-dismissible mt-3" role="alert">`,
      `   <div>${message}</div>`,
      '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
      '</div>'
    ].join('')
  
    camPosition.append(wrapper)
  }


//When exercise choice is confirmed, a form is submitted
form.addEventListener('submit', (e) => {
    // prevents default form submission 
    e.preventDefault();
    let exerciseId = form.elements["exerciseId"].value;
    console.log(typeof exerciseId);
    // calls python function to update exercise id
    socket.emit('changeExercise', exerciseId);
    // Make repCount and repFeedback visible

    repCount.style.display = 'flex';
    repFeedback.style.display = 'flex';
    
    summary.classList.remove("w-50", "fs-4", "card", "p-3", "mt-3");
    repInfo.style.display='flex';
    // Display camera position requirement as alert box
    // 0:Squat (Side)
    // 1:Squat (Front)
    // 2:Push-Up (Side)
    // 3:Push-Up (Front)
    let camPosReq = {};
    switch (exerciseId) {
        case '0':
            camPosReq = {exercise: "Squat (Side)", position:"table"};
            break;
        case '1':
            camPosReq = {exercise: "Squat (Front)", position:"table"};
            break;
        case '2':
            camPosReq = {exercise: "Push-Up (Side)", position:"ground"};
            break;
        case '3':
            camPosReq = {exercise: "Push-Up (Front)", position:"ground"};
            break;
    }
    alert(`Please place camera at ${camPosReq.exercise} height for ${camPosReq.position}`, 'warning');
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

toggleContainer.addEventListener('click', () => {
    if (toggleContainer.classList.contains('active')) {
        socket.emit('changeDifficulty', 'Beginner');
    }
    else {
        socket.emit('changeDifficulty', 'Expert');
    }
    toggleContainer.classList.toggle('active');
})

/*
navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(function(stream) {
        let mediaRecorder = new MediaRecorder(stream, {mimeType: "video/webm"});
        mediaRecorder.start();
        let chunks = [];
        mediaRecorder.ondataavailable = function(e) {
            chunks.push(e.data);
            console.log("Video data" + e.data);
        }
        mediaRecorder.onstop = function(e) {
            let blob = new Blob(chunks, { 'type' : 'video/webm; codecs=vp9' });
            chunks = [];
            let videoURL = window.URL.createObjectURL(blob);
            socket.emit('video', { 'video': true, 'buffer': videoURL });
        }
    })
    .catch(function(err) {
        console.log("An error occurred: " + err);
    });
*/
