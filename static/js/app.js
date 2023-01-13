
function getFeedback(feedback) {
    fetch(feedback.getAttribute('data-url')).then(response => {
        return response.json();
        
    }).then(data => {
        // data is the json data
        console.log("Test")
        let feedbackText = JSON.stringify(data);
        feedback.textContent = feedbackText;
    });
}

    const startButton = document.querySelector('.start-button');
    const endButton = document.querySelector('.end-button');
    const feedback = document.querySelector('#feedback');
    let started = false;

    startButton.addEventListener('click', (e) => {
        // runs python script that starts Peekingduck
        if (!started)
            {
            fetch(startButton.getAttribute('data-url'));
            startButton.style.display = "none";
            started = true;
            // updates feedback every second
            setInterval(getFeedback, 100, feedback);
        }
    });
    endButton.addEventListener('click', () => {
        fetch(endButton.getAttribute('data-url'));
        // adds the feedback to the div which displays it
        // waits for 2s
        setTimeout(getFeedback(feedback), 200);
    });







