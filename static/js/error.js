function getElementById(id) {
    return document.querySelector(`#${id}`);
}

function getElementByClass(className) {
    return document.querySelector(`.${className}`);
}

const sections = [
    getElementById('rep-time'),
    getElementById('squats-side'),
    getElementById('squats-front'),
    getElementById('push-up')
];

const navItems = [
    getElementByClass('rep-time-nav-item'),
    getElementByClass('squat-side-nav-item'),
    getElementByClass('squat-front-nav-item'),
    getElementByClass('push-up-nav-item')
];
