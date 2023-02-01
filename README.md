# National AI Student Challenge 2022
This is the GitHub Repo for the National AI Student Challenge 2022. We have used [PeekingDuck](https://github.com/aisingapore/PeekingDuck) as our core tool for Computer Vision.

To try our app immediately, you can click [this link](https://fitai.click), or you can click [this link](https://fitai.ddns.net) if the first link is not working.

If you have having trouble connecting, do confirm that you are using a secure connection (HTTPS, with a Lock sign on the browser) to connect to our website.

You can see the instructions at the [instructions page](https://fitai.click/instructions) of our site.

# To run our application yourself

There are *two modes* in which you can run our app in. 

The first is developer mode, where you can see the poses drawn onto the picture, and is used by us natively for testing/debugging. You can try out this mode to better understand how our model works.

The second is the production web server mode (unfortunately it can only support one connection at a time currently), which we intend to deploy to the cloud for the end-user, where they can use it on both Desktop and Mobile to aid in their exercise.

Please see the prequisites required for running our app in its respective modes.

## Prerequisites for Dev Mode
Running our app in development mode requires the installation of git, a Version Control Software (to clone the repository), as well as Python3 to run the code, and finally, a browser such as Google Chrome or Microsoft Edge which supports multi-part responses which are required to stream the PeekingDuck image data onto the web application.

### Installing Git  
Git can be installed by visiting [this link](https://git-scm.com/downloads).

### Installing Python
Python (Version 3.9) can be downloaded via [this link](https://www.python.org/downloads/).

### Installing a web browser that supports multi-part responses
Google Chrome can be downloaded via [this link](https://www.google.com/intl/en_sg/chrome/).

Microsoft Edge can be downloaded via [this link](https://www.microsoft.com/en-us/edge).

## To try out our app, please clone this git repository

This can be done by doing the following:

For Windows:  
Go to File Explorer and type cmd, and press Enter.  

Then paste ```git clone https://github.com/Yuheng3107/aichallenge``` into the command line (black screen that pops up).   
For macOS/Linux: Paste ```git clone https://github.com/Yuheng3107/aichallenge``` into the command line.

After cloning the git repository, there will be a new directory
called aichallenge created. 

You can move into that directory by typing ```cd aichallenge``` into the terminal.

In order to run our app, we highly recommend setting up a virtual environment in order to prevent conflicts in package dependencies. We shall be using [venv](https://docs.python.org/3/library/venv.html) for our app.

### To use the virtual environment (venv), there are 2 steps required:

1. Creating a virtual environment:  
Windows: ```py -3 -m venv venv```  
macOS/Linux: ```python3 -m venv venv```

2. Activating the virtual environment:  
Windows: ```venv\Scripts\activate```  
macOS/Linux: ```. venv/bin/activate```

When (venv) appears on the left of your terminal prompt, you have successfully installed and activated venv.

After this, run:
```pip3 install -r requirements.txt```
 to install the required dependencies for our app.  

Once the installation is successful, you can proceed to running our app using the terminal.

### Running the web server on your terminal (localhost)
To run the web server locally, either type  
```python3 app.py```  
or
```flask run```  
in the terminal.

If the server is successfully running, the prompt
```werkzeug  INFO:   * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)``` should appear on your terminal, and you can paste ```http://127.0.0.1:5000``` in your web browser (either Google Chrome or Microsoft Edge) to access the application web page.

### Run using Docker Containers (For Deployment on the Cloud i.e AWS or GCP or Azure, or you can do it locally to test it out)

Note: Cloud is recommended for those with more experience, otherwise you can try running the docker container locally.

First, you have to download Docker.

#### Setting up Docker on the Cloud
To run Docker on the Cloud (e.g EC2 instance on AWS), we can add the following code in our User data when launching a EC2 instance:
```
#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
```

Do note that the instance requires at least 2GiB of memory to run as CV is computationally intensive.

You can confirm that the Docker Daemon is running by running ```docker ps``` in the terminal and if ```CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES``` is returned, you can proceed to the next step.

#### Setting up Docker Locally
To download it locally, you can use [this link](https://www.docker.com/products/docker-desktop/) to download Docker Desktop.

Simply open the App, and run docker ps in the terminal to confirm that the Docker Daemon is running. If ```CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES``` is returned, you can proceed to the next step.

### Running the Docker Container
First, we need to pull the image from Docker Hub:

Paste ```docker pull yuheng3107/aichallenge:latest``` into the terminal (either cloud shell or locally).

It will take a while to pull the image from DockerHub, so please wait patiently for a few minutes or so until the download is complete before proceeding to the next step:

Run the Docker Container:
Paste ```docker run -p 5000:5000 yuheng3107/aichallenge``` into the terminal.

You can connect to the web server by pasting ```<your server's IP address/DNS hostname>:5000``` (Running on the Cloud), or ```http://127.0.0.1:5000``` (Running locally).

#### How it works
The Docker container is programmed to get image data from the front end and send it to the backend to be processed by PeekingDuck for the processing node to return the global feedback variables which the Flask Server and hence the front end can access by sending WebSocket requests in intervals.

It uses a custom input node called webcam.py which uses PeekingDuck's VideoNoThread class to read the jpeg frames provided by the front end with the Canvas API, and puts the img in the data pool, just like input.visual.

This was done because input.visual (which runs based on cv2.VideoCapture has no way of getting image data from the front end, as source=0 uses the camera in the backend (which servers/containers do not have), and hence a custom PeekingDuck node was made in collaboration with front end JS code to allow for this functionality).

# How to use the web app

After running the web server successfully and opening it in your chosen browser, you will be greeted with the following screen.

![Screenshot of UI](https://i.imgur.com/7Pu5RtJ.png "Web App UI")

To start exercising, do the following
1. Click on the green "Start Camera" button
2. Select an exercise from the drop down list, and then click "Start Exercise"
3. Position your camera according to the instruction in the yellow alert box.
4. Start doing the exercise. Verbal hints on how to improve your form for each rep will be read out by the browser
5. When you are done, cick on "End Exercise" to see a summary of your form. You can also click on "Show Feedback Log" so see the history of feedback on each of your reps.

