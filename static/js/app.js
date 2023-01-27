
function getFeedback() {
    socket.emit('feedback');
}

function getVideoFrames() {
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    let dataURL = canvas.toDataURL('image/jpeg');
    socket.emit('video', {'url': dataURL});
}


function setSpinner() {
    spinner.innerHTML = `<i class="fa fa-spinner fa-spin"></i>`;
}

// feedback interval in ms, updates feedback every 0.5s
const feedbackInterval = 500;



const startButton = document.querySelector('.start-button');
const endButton = document.querySelector('.end-button');
const repInfo = document.querySelector('#rep-info-group');
const repCount = document.querySelector('#rep-count');
const repFeedback = document.querySelector("#rep-feedback");
const feedback = document.querySelector('#feedback');
const form = document.querySelector('#changeExercise');
const showLogButton = document.querySelector("#show-log-button");
const feedbackList = document.querySelector('#feedback-list');
const mainFeedback = document.querySelector('#main-feedback');
const textToSpeechButton = document.querySelector('.text-to-speech');
const emotionFeedback = document.querySelector('#emotion-feedback');
const difficultyButton = document.querySelector('#difficulty');
const video = document.querySelector("#video");
const canvas = document.querySelector("#canvas");
const camPosition = document.querySelector("#cam-position");
const toggleContainer = document.querySelector(".toggle-container")  
const spinner = document.querySelector('#spinner');
const changeViewButtons = document.querySelectorAll('.change-view');

// need both buttons to be clickable especially for mobile users

/* Test Code to print all media devices for debugging */
navigator.mediaDevices.enumerateDevices().then(devices => {
    devices.forEach(device => {
        window.alert(`${device.kind}: ${device.label} id = ${device.deviceId}`);
    })
});


let synth;
let textToSpeech = false;
let loading = true;
let constraints = {
    video: {
    facingMode: "user"
    //  tries to get camera that faces user
  }
};


if ('speechSynthesis' in window) {
    synth = window.speechSynthesis;
    textToSpeech = true;
}
else {
    // replace with overlay and div pop-up in the future
    window.alert('text to speech not available');

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
        // runs python script that starts Peekingduck if PeekingDuck is not already running
        socket.emit('start');
        console.log("PeekingDuck running");
        startButton.style.display = "none";
        
        if ('mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices) {
            // checks that browser supports getting camera feed from user
            // if so use the getUserMedia API to get video from the user, after
            // asking for permission from the user


            navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
                // sizes the video to be same size as stream
                
                video.srcObject = stream;
                // sizes the canvas to be same size as the camera resolution
                let videoTracks = stream.getVideoTracks();
                while (true) {
                    if (videoTracks.length > 0) {
                        let settings = videoTracks[0].getSettings();
                        // set the video and canvas to the height and width of the stream
                        video.width = settings.width;
                        video.height = settings.height;
                        canvas.width = settings.width;
                        canvas.height = settings.height;
                        break;
                    }
                }
                // sends jpeg to backend at 25 fps
                setInterval(getVideoFrames, 40);
            }).catch(function(err) {
                console.log("An error occurred: " + err);
            });
          }
          else {
              window.alert("getUserMedia API not supported on your browser");
          }
        

        started = true;

        // updates feedback every 0.5s
        setInterval(getFeedback, feedbackInterval);
        // adds spinner at same time as feedback is updated
        setTimeout(setSpinner, feedbackInterval);
    }
});
endButton.addEventListener('click', () => {
    socket.emit('endExercise');
    mainFeedback.classList.add("w-50", "fs-4", "card", "p-3", "mt-3");
    repInfo.style.display='none';
    console.log('end button clicked');
});

const alert = (message, type) => {

    camPosition.innerHTML = [
      `<div class="alert alert-${type} alert-dismissible mt-3" role="alert">`,
      `   <div>${message}</div>`,
      '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
      '</div>'
    ].join('')

    // refactored so only one alert shows
  }


//When exercise choice is confirmed, a form is submitted
form.addEventListener('submit', (e) => {
    // prevents default form submission 
    e.preventDefault();
    let exerciseId = form.elements["exerciseId"].value;
    // calls python function to update exercise id
    socket.emit('changeExercise', exerciseId);
    // Make repCount and repFeedback visible

    repCount.style.display = 'flex';
    repFeedback.style.display = 'flex';
    
    mainFeedback.classList.remove("w-50", "fs-4", "card", "p-3", "mt-3");
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
    alert(`Please place camera at ${camPosReq.position} height for ${camPosReq.exercise}`, 'warning');
});

// Listens for feedback event from server which updates
// front end 
socket.on('feedback', (stringData) => {
    let data = JSON.parse(stringData);
    // if repCount changes, update text display on screen
    if (Number(repCount.textContent) != data["repCount"]) {
        // update repCount
        repCount.textContent = data["repCount"];
        repFeedback.textContent = data.repFeedback.slice(-1);
        //append list items to the feedback log
        let li = document.createElement('li');
        li.innerText = data.repFeedback.slice(-1);
        feedbackList.insertBefore(li, feedbackList.firstChild);

        if (textToSpeech) {
            // if text to speech available, speak most recent rep 
            let speech = new SpeechSynthesisUtterance(feedbackList.firstChild.innerText);
            synth.speak(speech);
        }
    }
    
    // Check whether peekingduck pipeline is still loading
    // faster to check bool than string, reduce lag, short-circuit first arg
    if (loading && data.mainFeedback != "Loading...") {
        // if it has finished loading, remove spinner
        spinner.innerHTML = "";
        loading = false;
    }
    mainFeedback.innerText = data.mainFeedback
    emotionFeedback.innerText = data.emotionFeedback;
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


// Listens for disconnect events

window.onbeforeunload = () => {
    socket.emit('disconnect');
}

// Flips camera when button is clicked
changeViewButtons.forEach(button => {
    button.addEventListener('click', () => {
        // toggle between front and back camera
        if (constraints.video.facingMode == "user") {
            constraints.video.facingMode = "environment";
        }
        else if (constraints.video.facingMode == "environment") {
            constraints.video.facingMode = "user";
        }
        
        navigator.mediaDevices.getUserMedia(constraints).then(stream => {
            video.srcObject = stream;
            // modifies video source to be new stream, and at the same time removes old stream
        });
    });
});

// Listens to change in screen orientation and changes video height and width to suit the change
ScreenOrientation.onchange = function(e) {
    window.alert(`${video.height}, ${video.width}`);
    [video.height, video.width] = [video.width, video.height];
    window.alert(`${video.height}, ${video.width}`);
    [canvas.height, canvas.width] = [video.height, video.width];
}

/*
window.addEventListener("orientationchange", () => {
    // code to run when the screen orientation changes
    window.alert(`${video.height}, ${video.width}`);
  
    window.alert(`${video.height}, ${video.width}`);
    
  });
*/
  screen.orientation.addEventListener("change", function() {
    [canvas.height, canvas.width] = [video.height, video.width];
    [video.height, video.width] = [video.width, video.height];
  });