# aichallenge
GitHub Repo for National AI Student Challenge 2022

Please make sure your whole body is in view while doing the exercise

### To use virtual environment, there are 2 steps:

1. Creating a virtual environment:
Windows: py -3 -m venv venv
macOS/Linux: python3 -m venv venv

2. Activating the virtual environment
Windows: venv\Scripts\activate
macOS/Linux: . venv/bin/activate

After this, run:
pip3 install -r requirements.txt to install dependencies

### Run using Docker Containers
Pull the image from Docker Hub:
docker pull yuheng3107/aichallenge:latest

Run the Docker Container using:
docker run -p 5000:5000 yuheng3107/aichallenge
