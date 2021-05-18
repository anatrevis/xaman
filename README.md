# Requirements: 
Install Anaconda to create an env 
python 3.8.0 
chatterbot 1.0.1 
pip install Flask 
pip install pyowm

# How to run

## Option 1) After installing requirements:

run application: python application.py
run tests: python test_chatbot.py -v


## Option 2) Create env with Conda from environment.yml:
1) Install Anaconda: https://docs.anaconda.com/anaconda/install/
2) conda env create --file environment.yml (note: change the path at the end of .yml file)
3) conda activate environment
4) run application: python application.py
5) run tests: python test_chatbot.py -v
