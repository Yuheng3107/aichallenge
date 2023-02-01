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

const navItems = {
    'rep-time': getElementByClass('rep-time-nav-item'),
    'squats-side': getElementByClass('squat-side-nav-item'),
    'squats-front': getElementByClass('squat-front-nav-item'),
    'push-up': getElementByClass('push-up-nav-item')
};

// set up observer
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0,
  };

  function observerCallback(entries, observer) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // get the nav item corresponding to the id of the section
        // that is currently in view
        const navItem = navItems[entry.target.id];
        // add 'active' class on the navItem
        navItem.classList.add('active');
        // remove 'active' class from any navItem that is not
        // same as 'navItem' defined above
        Object.values(navItems).forEach((item) => {
          if (item != navItem) {
            item.classList.remove('active');
          }
        });
      }
    });
  }

const observer = new IntersectionObserver(observerCallback, observerOptions);

sections.forEach((sec) => observer.observe(sec));