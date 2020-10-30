# BirmingHome

## Description
BirmingHome is a home service website similar to NextDoor where you post requests for household jobs that you need help with. You have to create a profile to post jobs and to see other posts and user profiles. You can filter posts by location or by job type. You can edit your profile to update your phone number, profile picture, or about me. You can view other user’s profiles when they post a job request so that you can get their contact info. 

## Set Up Instructions
This project was built in a Flask environment. To use Flask, you have to download and install Andaconda which can be done at this link: https://www.anaconda.com/distribution/. During installation, select "add anaconda to my path environment variable".

Next, open the terminal and navigate to this project folder. Type:```conda create -n flaskenv python=3.7```
Then, type y for yes.

Next, you have to activate the Flask environment.
For windows type: ```activate flaskenv```
For mac/linux type: ```source activate flaskenv```
(type deactivate or conda deactivate to exit)

Next, type ```pip install -r requirements.txt``` to install all the libraries.

Now, you are ready to run the website. Type ```python main.py``` to start the server.
Then, go to http://127.0.0.1:5000/ in your browser! 