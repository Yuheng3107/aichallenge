// IMPT FUNCTIONS
////////

// feedback interval in ms, updates feedback every 0.5s
const feedbackInterval = 500;
function getFeedback() {
    // get feedback while app is running
    socket.emit('feedback');
}

function getVideoFrames() {
    // send video to backend, draw on frontend
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    let dataURL = canvas.toDataURL('image/jpeg', 0.1);
    socket.emit('video', {'url': dataURL});
}

// check if browser is mobile (cause mobile has weird resizing of image)
window.mobileCheck = function() {
    let check = false;
    (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
    return check;
};

// WEBPAGE OBJECTS
////////

// buttons
const startButton = document.querySelector('#start-button');
const startButtonGroup = document.querySelector('#start-button-group');
// form is the startExercise button form
const form = document.querySelector('#changeExercise');
const endButton = document.querySelector('#end-button');
const showLogButton = document.querySelector("#show-log-button");
const feedbackButton = document.querySelector('#feedback-button');
// buttons-navbar
const textToSpeechButton = document.querySelector('.text-to-speech');
const difficultyButton = document.querySelector('#difficulty');
const changeViewButtons = document.querySelectorAll('.change-view'); 

// feedback
const repInfo = document.querySelector('#rep-info-group');
const repCount = document.querySelector('#rep-count');
const repFeedback = document.querySelector("#rep-feedback");
const feedback = document.querySelector('#feedback');
const feedbackList = document.querySelector('#feedback-list');
const mainFeedback = document.querySelector('#main-feedback');
const emotionFeedback = document.querySelector('#emotion-feedback');

// misc
const alerter = document.querySelector("#alerter");
const video = document.querySelector("#video");
const canvas = document.querySelector("#canvas");
const toggleContainer = document.querySelector(".toggle-container")  

// bootstrap alerts
const alert = (message, type) => {
    alerter.innerHTML = [
      `<div class="alert alert-${type} alert-dismissible mt-3" role="alert">`,
      `   <div>${message}</div>`,
      '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
      '</div>'
    ].join('')
}

// BROWSER CHECK
////////

let userAgent = navigator.userAgent;
let browserName = "others";
if (userAgent.match(/chrome|chromium|crios/i)){
    browserName = "chrome";
} else if (userAgent.match(/firefox|fxios/i)){
    browserName = "firefox";
}   else if (userAgent.match(/safari/i)){
    browserName = "safari";
} else if (userAgent.match(/opr\//i)){
    browserName = "opera";
}  else if (userAgent.match(/edg/i)){
    browserName = "edge";
} else {
    browserName="No browser detection";
}

// BOOLS
////////

let loading = true;
// is application loading?
let exerciseStarted = false;
// currently in exercise
let constraints = {
    video: {
    facingMode: "user"
    // tries to get camera that faces user
  }
};
let firstTimeLoading = true;

let synth;
// narrator
let textToSpeech = false;
// toggle for narrator
if ('speechSynthesis' in window) {
    synth = window.speechSynthesis;
    textToSpeech = true;
}
else {
    // replace with overlay and div pop-up in the future
    window.alert('text to speech not available','info');
}
let started = false;
// initialises io with namespace /app
let socket = io("/app");
let mainSocket = io();




// ON LOAD
////////

document.addEventListener('DOMContentLoaded', (event) => {
    // hide unnecessary buttons and feedback on page load

    if (!repCount.textContent) {
        repCount.style.display = 'none';
    }
    if (!repFeedback.textContent) {
        repFeedback.style.display = 'none';
    }
    endButton.style.display = 'none';
    form.style.display = 'none';
    feedbackButton.style.display = 'none';
    showLogButton.style.display = 'none';
})




// EXERCISE BUTTONS
////////

startButton.addEventListener('click', (e) => {
    // when start button is pressed, send event to backend, 
    // do front end start processes, change ui

    console.log('start button clicked');
    if (!started) {
        // runs python script that starts Peekingduck if PeekingDuck is not already running
        started = true;
        socket.emit('start');
        console.log("PeekingDuck running");

        // hide the start button group
        startButtonGroup.style.display = 'none'; 
        showLogButton.style.display = 'block';

        // start AFK check
        inactivityTime()

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
                        if (window.mobileCheck() && (browserName == "safari" || browserName == "firefox"))
                        {
                            // flip images on mobile to make backend image have correct resolution cause mobile is weird
                            video.width = settings.height;
                            video.height = settings.width;
                            canvas.width = settings.height;
                            canvas.height = settings.width;
                        }
                        else {
                            video.width = settings.width;
                            video.height = settings.height;
                            canvas.width = settings.width;
                            canvas.height = settings.height;
                        }
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
              window.alert("getUserMedia API not supported on your browser", 'danger');
          }
        // updates feedback every 0.5s
        setInterval(getFeedback, feedbackInterval);
    }
});

endButton.addEventListener('click', () => {
    // when exercise ends, send event to backend,
    // change ui

    socket.emit('endExercise');

    // hide rep feedback and end button 
    endButton.style.display = 'none';
    repInfo.style.display = 'none';
    console.log('end button clicked');

    // make startExercise form, link to errors appear
    form.style.display = 'flex';
    feedbackButton.style.display = 'block';

    // display main feedback instead of technical errors
    mainFeedback.classList.add("fs-4", "card", "p-3", "mt-3");
});

form.addEventListener('submit', (e) => {
    // When exercise choice is confirmed, send event to backend, 
    // change ui, display alert

    // prevents default form submission 
    e.preventDefault();

    // calls python function to update exercise id
    let exerciseId = form.elements["exerciseId"].value;
    socket.emit('changeExercise', exerciseId);

    // Make repCount and repFeedback visible
    repCount.style.display = 'flex';
    repFeedback.style.display = 'flex';
    endButton.style.display = 'block';

    // Hide start exercise button, link to errors
    form.style.display = 'none';
    feedbackButton.style.display = 'none';
    
    // mainFeedback becomes technical errors
    mainFeedback.classList.remove("fs-4", "card", "p-3", "mt-3");
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
    // camera position prompt
    alert(`Please place camera vertically at ${camPosReq.position} height for ${camPosReq.exercise}`, 'warning');
});



// SECONDARY BUTTONS
////////

showLogButton.addEventListener('click', (event) => {
    // When log button is pressed, toggle rep log

    showLogButton.classList.toggle('active');
    feedbackList.classList.toggle('active');
    if (showLogButton.classList.contains("active")) {
        showLogButton.children.childNodes[0].textContent = "Hide Feedback Log";
    } else {
        showLogButton.children.childNodes[0].textContent = "Show Feedback Log";
    }
})

textToSpeechButton.addEventListener('click', () => {
    // toggle narrator

    if (textToSpeech) {
        textToSpeech = false;
        textToSpeechButton.classList.remove('btn-danger');
        textToSpeechButton.classList.add('btn-success');
        textToSpeechButton.innerText = "Enable Text-To-Speech";
    }
    else {
        textToSpeech = true;
        textToSpeechButton.classList.remove('btn-success');
        textToSpeechButton.classList.add('btn-danger');
        textToSpeechButton.innerText = "Disable Text-To-Speech";
    }
})

toggleContainer.addEventListener('click', () => {
    // change difficulty

    if (toggleContainer.classList.contains('active')) {
        socket.emit('changeDifficulty', 'Beginner');
    }
    else {
        socket.emit('changeDifficulty', 'Expert');
    }
    toggleContainer.classList.toggle('active');
})

changeViewButtons.forEach(button => {
    // Flips camera when button is clicked

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



// RECIEVE DATA FROM BACKEND
////////

socket.on('feedback', (stringData) => {
    // Listens for feedback event from server,
    // which updates front end data

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

    // sentimental analysis
    emotionFeedback.innerText = data.emotionFeedback; 

    // check if loading
    if (!loading) {
        // update main feedback
        mainFeedback.innerText = data.mainFeedback;
        return;
    } 
    
    // loads spinner if it is first time loading
    if (firstTimeLoading && data.mainFeedback == "Loading...") {
        mainFeedback.innerHTML = `<i class="fa fa-spinner fa-spin"></i>&nbsp;${data.mainFeedback}`;
        firstTimeLoading = false;
        return;
    }
    // Check whether peekingduck pipeline is still loading
    // faster to check bool than string, reduce lag, short-circuit first arg
    if (loading && data.mainFeedback != "Loading...") {
        loading = false;
        // display start exercise form
        form.style.display = "flex";
    }
}) 

socket.on('kickout', () => {
    // kicks everyone out when someone runs a PeekingDuck instance 
    if (!started) {
        window.location.href += "lobby";
    }
})

mainSocket.on('forceKickout', () => {
    // force kick for server reset 
    window.location.href += "lobby";
})

socket.on('disconnect', () => {
    // disconnect
    alert("Error: Disconnected. Please refresh the page.",'danger');
}) 



// MISC FUNCTIONS
////////

// change mobile screen orientation if it is mobile
if (window.mobileCheck()) {
    window.addEventListener('resize', resizing);
}

let innerWidth = window.innerWidth;
function resizing() {
    // if orientation change and it's mobile, resize camera output
    if (innerWidth === window.innerWidth) return;
    innerWidth = window.innerWidth;
    if(window.innerWidth > window.innerHeight) {
        [canvas.height, canvas.width] = [canvas.width, canvas.height];
        [video.height, video.width] = [video.width, video.height];
    }
    if(window.innerWidth < window.innerHeight) {
        [canvas.height, canvas.width] = [canvas.width, canvas.height];
        [video.height, video.width] = [video.width, video.height];
    }
}

let inactivityTime = function () {
    //AFK check

    let time;
    let almostTime;

    // actions to reset logout timer
    window.onload = resetTimer;
    document.onclick = resetTimer;
    document.onmousemove  = resetTimer;

    function logout() {
        // reload page to logout user after 5 mins of inactivity

        location.reload();
    }
    function almostLogout() {
        // alert user that they are AFK 1 min before kick out

        alert("Inactivity detected. You will be logged out in 1 min if action is not detected.",'danger');
    }
    function resetTimer() {
        // on action, reset timer

        clearTimeout(time);
        clearTimeout(almostTime);

        // at 5 mins, logout
        time = setTimeout(logout, 300000);

        // at 4 mins, alert
        almostTime = setTimeout(almostLogout, 240000);
    }
};
