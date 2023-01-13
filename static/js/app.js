
window.addEventListener('DOMContentLoaded', (event) => { //Wait for the DOM tree to render out before running allowing interaction
    const startButton = document.querySelector('.start-button');
    const endButton = document.querySelector('.end-button');
    let started = false;

    startButton.addEventListener('click', (e) => {
        // runs python script that starts Peekingduck
        if (!started) {
            fetch(startButton.getAttribute('data-url'));
            started = true;
        }

    });
    endButton.addEventListener('click', () => {
        fetch(endButton.getAttribute('data-url'));
    });

})





