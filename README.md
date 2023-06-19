![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![Repo Size](https://img.shields.io/github/repo-size/Sulstice/global-chem)
[![PyPI version](https://badge.fury.io/py/global-chem.svg)](https://badge.fury.io/py/global-chem)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
# C-4PM: A Conversational agent for declarative Process Mining

C-4PM is a conversational interface for Declarative Process Mining. 
It allows users to interact with a declarative process specification and its corresponding event log
to perform multiple reasoning tasks.

## Abstract

## Installation

### Basic requirements

> **_NOTE:_**  Creating a virtual environment is highly recommended. For best compatibility this 
> should be done using Python 3.10 as `python3.10 -m venv ./venv`. If you don't have Python 3.10 installed,
> you can do it (in MacOS) with `brew install python@3.10`

- Python version: 3.10
- Docker needs to be installed
- [Lydia]() needs to be installed and configured. Logaut needs to be installed
- [NL2LTL]() is shipped within C-4PM (no need for separate installation)
- The rest of the required libraries can be installed with `pip install -r requirements.txt`

### Installation steps

### Training and using your own model

You can train a new model adapted to your use case by running the command `rasa train` in the project root folder.
This will use files `domain.yml`, `config.yml`, `credentials.yml`, `endpoints.yml`, `data/nlu.yml` `data/rules.yml` 
and `data/stories.yml` to train a new model.
These files hold all the relevant information to train a language model for your conversational agent. 
For more information on how to do this, please read [Rasa's docs](https://rasa.com/docs/rasa/tuning-your-model/)

You can use the model you just trained by modifying the path in the variable `model_path` in `main.py` 
with the corresponding name of your model.

For training a NL2LTLf Rasa model with your own data, you can do this by running the command 
`rasa train --config data/config.yml --domain data/domain.yml --data data/nlu_training.yml` 
in the directory `nl2ltl/engines/rasa`.

### Running

To run the conversational agent you need to run:
- A Rasa actions server. This can be done with by running the command `rasa run actions` in the `actions` folder inside the project root folder `cd actions`.
- A Docker container with [Duckling](https://hub.docker.com/r/rasa/duckling) running. 
Duckling is used to parse things like emails, dates, temporal intervals and more.
- 


## Sample conversations

## Modifications to source libraries

### LTLf2DFA
- Adapted GPT prompt and RASA NLU training data to these proposal's objectives.
- Added support to the "absence" Declare template in the GPT `prompt`

### Declare4Py
- Added support to the "absence" template in `LTLModel.py`so the absence concept can be used in different reasonin tasks.

