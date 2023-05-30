# StackOverflow-Lite
[![Travis Build](https://img.shields.io/travis/winniejerop/StackOverflow-Lite.svg?style=popout)](https://travis-ci.org/winniejerop/StackOverflow-Lite)
[![Coverage Status](https://coveralls.io/repos/github/winniejerop/StackOverflow-Lite/badge.svg?branch=master)](https://coveralls.io/github/winniejerop/StackOverflow-Lite?branch=master)
[![Codeclimate](https://img.shields.io/codeclimate/maintainability-percentage/angular/angular.js.svg?style=popout)](https://codeclimate.com/github/winniejerop/StackOverflow-Lite)

# Project Overview
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

# Hosted on GitHub pages
https://winniejerop.github.io/StackOverflow-Lite/


# Installation
To install:
- git clone https://github.com/winniejerop/StackOverflow-Lite.git
- cd StackOverflow-Lite
- virtualenv venv
- venv\Scripts\activate (Windows OS)
- install requirements.txt
- python index.py 

# Testing
pytest
unittest

# Challenge 2 - Setup API Endpoints 
# Api Endpoints
# Installation
To install:
- git clone https://github.com/winniejerop/StackOverflow-Lite.git
- cd StackOverflow-Lite
- virtualenv venv
- venv/Scripts/activate (Windows)
- pip install requirements.txt
- python run.py 

# Api Endpoints
/api/v1/questions (get all questions)

/api/v1/questions (post a question)

/api/v1/questions/001

/api/v1/questions/1:001/answer

# Challenge 3 - Setup API endpoints and secure them using JWT
# Installation
To install:
- git clone https://github.com/winniejerop/StackOverflow-Lite.git -b challenge_3
- cd StackOverflow-Lite
- virtualenv venv
- venv/Scripts/activate (Windows)
- pip install requirements.txt
- python manage.py 

# Hosted on Heroku
https://stackoverflow-lite-ch3.herokuapp.com/

# Apiary Documentation
https://stackoverflowlite12.docs.apiary.io/#


# Api Endpoints
POST /api/v1/auth/signup

POST /api/v1/auth/login

POST /api/v1/auth/logout

GET /api/v1/questions 

GET /api/v1/questions/1

POST /api/v1/questions/1/answer

PUT /api/v1/questions/1/answers/1


