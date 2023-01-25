# National AI Student Challenge 2022
This is the GitHub Repo for the National AI Student Challenge 2022. We have used [PeekingDuck](https://github.com/aisingapore/PeekingDuck) as our core tool for Computer Vision.

## Prerequisites
Running our app requires the installation of git, a Version Control Software (to clone the repository), as well as Python3 to run the code, and finally, a browser such as Google Chrome or Microsoft Edge which supports multi-part responses which are required to stream the PeekingDuck image data onto the web application.

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

In order to run our app, we highly recommend setting up a virtual environment, in order to prevent conflicts in package dependencies. We shall be using [venv](https://docs.python.org/3/library/venv.html) for our app.
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
```werkzeug  INFO:   * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)``` should appear on your terminal, and you can paste http://127.0.0.1:5000 in your web browser (either Google Chrome or Microsoft Edge) to access the application web page.

### Run using Docker Containers (For Deployment on the Cloud i.e AWS or GCP or Azure, or you can do it locally to test it out)
Pull the image from Docker Hub:
```docker pull yuheng3107/aichallenge:latest```

Run the Docker Container:
```docker run -p 5000:5000 yuheng3107/aichallenge```


The Docker container is programmed to get image data from the front end and send it to the backend to be processed by PeekingDuck and finally sent back to the front end after it goes through the pipeline of nodes.

It uses a custom 

Currently, the docker container is unable to connect when HTTPS is enabled.

# How to use the web app

After running the web server using *flask run* and opening it in your chosen browser, you will be greeted with the following screen.

![Screenshot of UI](https://i.imgur.com/7Pu5RtJ.png "Web App UI")

To start exercising, do the following
1. Click on the green "Start Camera" button
2. Select an exercise from the drop down list, and then click "Start Exercise"
3. Position your camera according to the instruction in the yellow alert box.
4. Start doing the exercise. Verbal hints on how to improve your form for each rep will be read out by the browser
5. When you are done, cick on "End Exercise" to see a summary of your form. You can also click on "Show Feedback Log" so see the history of feedback on each of your reps.

