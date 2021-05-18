# Introduction:
Xaman is a chatbot developed in the context of a project in the Software Development 2 module of the second year of the Computer Science Bachelors Honors Part-Time course at Griffith College Dublin. The bot's name was inspired by the mystical councilors of ancient Asian tribes, called "Shamans".

Shamans were thought to have a special connection with spirits and the Mother Nature, making it possible for them to discover the cause of illness,  bad luck,  predict the weather, and even the future. Xaman still doesn't have all of such talents. But, it can predict the weather for any destination in the world within five days with precision and advise appropriate clothes for wearing on the trip to this place.

Xaman was developed in Python using Chatterbot, a machine-learning-based library that structures the "brain" of the bot's artificial intelligence. 


# Requirements: 
- python 3.8.0 
- chatterbot 1.0.1 
- pip install Flask 
- pip install pyowm

*note: you can install Anaconda to create a virtual env with Python 3.8.0 and all the requirements. Refer to Option 2 on How to run.

# How to run

## Option 1) After installing requirements:

run application: python application.py
run tests: python test_chatbot.py -v


## Option 2) Create env with Conda from environment.yml:
1) Install Anaconda: https://docs.anaconda.com/anaconda/install/
2) conda env create --file environment.yml 
3) conda activate environment
Then, run normally:
4) run application: python application.py
5) run tests: python test_chatbot.py -v

*note: change the path at the end of environment.yml file
