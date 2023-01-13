

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
        }
        

    });
    endButton.addEventListener('click', () => {
        fetch(endButton.getAttribute('data-url'));
        // adds the feedback to the div which displays it
        fetch(feedback.getAttribute('data-url')).then(response => {
            return response.json();
            
        }).then(data => {
            // data is the json data
            let feedbackText = JSON.stringify(data);
            feedback.textContent = feedbackText;
        });
    });







