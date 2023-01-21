# aichallenge
This is the GitHub Repo for the National AI Student Challenge 2022

Please make sure your whole body is in view while doing the exercise

### Prerequisites
Running our app requires the installation of git (to clone the repo), as well as Python to run the code, as well as a Chromium-based browser such as Google Chrome, or Microsoft Edge so you can use the web app.

Git can be installed by visiting this link:
https://git-scm.com/downloads

Python (Version 3.9) can be downloaded via this link:
https://www.python.org/downloads/

Google Chrome can be downloaded via this link:
https://www.google.com/intl/en_sg/chrome/

Microsoft Edge can be downloaded via this link:
https://www.microsoft.com/en-us/edge

### To try out our app, please clone this git repository

This can be done by doing the following:

Windows: Go to File Explorer and type cmd, and enter,
         then paste https://github.com/Yuheng3107/aichallenge
         into the command line

macOS/Linux: Paste https://github.com/Yuheng3107/aichallenge
            into the command line

After cloning the git repository, there will be a new directory
called aichallenge created. 

You can move into that directory by typing cd aichallenge into the terminal.

### To use virtual environment, there are 2 steps:

1. Creating a virtual environment:
Windows: py -3 -m venv venv
macOS/Linux: python3 -m venv venv

2. Activating the virtual environment
Windows: venv\Scripts\activate
macOS/Linux: . venv/bin/activate

After this, run:
pip3 install -r requirements.txt to install dependencies

### Run using Docker Containers (WIP as HTTPS is not working on Docker Containers because of self-signed SSL Certificate)
Pull the image from Docker Hub:
docker pull yuheng3107/aichallenge:latest

Run the Docker Container using:
docker run -p 5000:5000 yuheng3107/aichallenge

Note: Docker container is unable to get camera from source=0,
it has to get from front end but doing so requires HTTPS connection.

Currently, the docker container is unable to connect when HTTPS is enabled.