# StackOverflow-Lite
StackOverflow-lite is a platform where people can ask questions and provide answers.

# Required Features
1. Users can create an account and log in.
2. Users can post questions.
3. Users can delete the questions they post
4. Users can post answers
5. Users can view the answers
6. Users can accept an answer out of all the answers to his/her queston as they preferred answer

# Challenge 1 - Create UI Templates
Complete UI Pages
1. Signup and signin pages
2. Questoins list page
3. View questions and Answers page
4. Post question page
5. User profile page
6. Host UI template on github pages 

# Installation
To install:
git clone https://github.com/winniejerop/StackOverflow-Lite.git
cd StackOverflow-Lite
virtualenv venv
venv/Scripts/activate (Windows)
pip install requirements.txt
python index.py 

# Testing
pytest
unittest

# Challenge 2 - Setup API Endpoints 
# Api Endpoints

/api/v1/questions
/api/v1/questions/001
/api/v1/questions/1:001/answer
