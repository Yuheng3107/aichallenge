
function getFeedback(feedback, repCount) {
    fetch(feedback.getAttribute('data-url')).then(response => {
        return response.json();

    }).then(data => {
        // data returned from backend is an array
        console.log(data[0]);
        repCount.textContent = data[0];
        feedback.textContent = data.slice(1);
    });
}

const startButton = document.querySelector('.start-button');
const endButton = document.querySelector('.end-button');
const repCount = document.querySelector('#rep-count');
const feedback = document.querySelector('#feedback');
let started = false;

startButton.addEventListener('click', (e) => {
    // runs python script that starts Peekingduck
    if (!started) {
        fetch(startButton.getAttribute('data-url'));
        startButton.style.display = "none";
        started = true;
        // updates feedback every second
        setInterval(getFeedback, 1000, feedback, repCount);
    }
});
endButton.addEventListener('click', () => {
    fetch(endButton.getAttribute('data-url'));
    // adds the feedback to the div which displays it
    // waits for 2s
    setTimeout(getFeedback(feedback), 2000);
});







