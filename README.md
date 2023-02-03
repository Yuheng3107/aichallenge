# National AI Student Challenge 2022
This is the GitHub Repo for the National AI Student Challenge 2022. We have used [PeekingDuck](https://github.com/aisingapore/PeekingDuck) as our core tool for Computer Vision.

To try our app immediately, you can click [this link](https://fitai.click), or you can click [this link](https://fitai.ddns.net) if the first link is not working. Do note that the second link will warn you that your connection is not private. Click on advanced and proceed to the website.

If you have having trouble connecting, do confirm that you are using a secure connection (HTTPS, with a Lock sign on the browser) to connect to our website.

You can see the instructions at the [instructions page](https://fitai.click/instructions) of our site.

# To run our server yourself
Running our server requires the installation of git, a Version Control Software (to clone the repository), as well as Python3 to run the code, TensorFlow for GPU integration, and finally, a browser such as Google Chrome or Microsoft Edge which supports multi-part responses which are required to stream the PeekingDuck image data onto the web application. 

### Specs
The server requires a GPU and around 3GB of Ram. It can be run on a CPU, but performance will be much worse. Accuracy of the programme is not guaranteed on a CPU.

### Installing Git
Git can be installed by visiting [this link](https://git-scm.com/downloads).

### Installing Python
Python (Version 3.9) can be downloaded via [this link](https://www.python.org/downloads/).

### Installing TensorFlow
You can view TensorFlow's guide for installation via [this link](https://www.tensorflow.org/install/pip).

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

In order to run our app, we highly recommend setting up a virtual environment in order to prevent conflicts in package dependencies. If you followed the TensorFlow tutorial, you should now have a conda virtual environment set up.

Creating a virtual environment: 
```conda create --name tf python=3.9```  

Activating the virtual environment:  
```conda activate tf```  

Deactivating the virtual environment:
```conda deactivate``` 

### Setting up your Virtual Environment

After this, run:
```conda install cuda-nvcc``` and 
```pip install -r requirements.txt```
 to install the required dependencies for our app.  

Once the installation is successful, you can proceed to running our app using the terminal.

### Running the web server on your terminal
To run the web server locally, type ```python3 app.py``` in the terminal.

If the server is successfully running, the prompt
```werkzeug  INFO:   * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)``` should appear on your terminal, and you can paste ```http://127.0.0.1:5000``` in your web browser (either Google Chrome or Microsoft Edge) to access the application web page.

### Allowing other people to connect to your web server.
You may view a guide on how to port forward via [this link](https://www.lifewire.com/how-to-port-forward-4163829).
