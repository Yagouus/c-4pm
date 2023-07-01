![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![Repo Size](https://img.shields.io/github/repo-size/Sulstice/global-chem)
[![PyPI version](https://badge.fury.io/py/global-chem.svg)](https://badge.fury.io/py/global-chem)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
# C-4PM: A Conversational agent for declarative Process Mining

C-4PM is a conversational interface for Declarative Process Mining. 
It allows users to interact with a declarative process specification and its corresponding event log
to perform multiple reasoning tasks.

## Abstract

The effective presentation of process models to non-expert users in a way that allows them to understand
and query these models is a well-known research challenge. Conversational interfaces, with their low
expertise requirements, offer a potential solution. While procedural models like Petri nets are not ideal
for linguistic presentation, declarative models, specifically the Declare specification, provide a more
suitable option. This paper introduces C-4PM, the first conversational interface for declarative process
specifications. C-4PM facilitates tasks such as consistency, conformance, and model checking through a
conversation-driven modular pipeline. The feasibility of the tool was assessed through a preliminary
evaluation on a healthcare process.

## Interactive and video demo
- An **interactive demo** of the tool can be tested at: http://tec.citius.usc.es/aos2text 
(if the demo seems not to be working, please [get in touch](mailto:yago.fontenla.seco@usc.es))
- A **video demonstration** of the tool can be found in the following link: 

## Installation

> **_NOTE:_**  Creating a virtual environment is highly recommended. For best compatibility this 
> should be done using Python 3.10 as `python3.10 -m venv ./venv`. If you don't have Python 3.10 installed,
> you can do it (in MacOS) with `brew install python@3.10`

### Basic requirements

- **Python** version: 3.10 (`brew install python@3.10`)
- **Docker** needs to be installed (`brew install docker`)
- [**Lydia**](https://github.com/whitemech/lydia) needs to be installed and configured with docker. 
To do so, we recommend the [logaut guide](https://pypi.org/project/logaut/).
- The rest of the **required libraries** can be installed with `pip install -r requirements.txt`.
- Sometimes, due to you own machine configuration, some packages listed in  `requirements.txt` may not install correctly.
As this project was built in a MacOS machine, some dependencies are specifically for MacOs (e.g.: `tensorflow`). 
If you receive some errors during the installation, please, check the dependencies that are causing these errors and
delete/modify them correctly in the requirements file or install those packages by hand with `pip install package-name`.

### Training and using your own model

You can train a new model adapted to your use case by running the command `rasa train` in the project's root folder.
This will use files `domain.yml`, `config.yml`, `credentials.yml`, `endpoints.yml`, `data/nlu.yml` `data/rules.yml` 
and `data/stories.yml` to train a new model.
These files hold all the relevant information to train a language model for your conversational agent. 
For more information on how to do this, please read [Rasa's docs](https://rasa.com/docs/rasa/tuning-your-model/).

If you want to run C-4PM as is, just run the command `rasa train` in the project's root folder. 
Once trained, the model will be in the `models/` directory.

To use the model you've just trained you need to modify variable `model_path` in `main.py` or 
`main_server.py` with the corresponding name of your model e.g.:
`model_path = 'models/20230630-105642-tractable-cheetah.tar.gz`.

> **_NOTE:_**   NL2LTL can be used with a RASA engine or GPT. In this particular case, the GPT engine is used.
> However, if you want to use the RASA engine, for training a customized RASA language model with your own data, 
> you can do this by running the command 
> `rasa train --config data/config.yml --domain data/domain.yml --data data/nlu_training.yml` 
>in the directory `nl2ltl/engines/rasa`. More information can be found in the [NL2LTL repository](https://github.com/IBM/nl2ltl)

### Running
The conversational agent can run in to modes, if you want to run it in a local machine, or you want to deploy it 
as an online accessible demo:

**Running C-4PM locally**

To run the conversational agent you need to run:
- A Rasa actions server. This can be done with by running the command `rasa run actions` in the `actions` folder inside the project root folder `cd actions`.
- A Docker container with [Duckling](https://hub.docker.com/r/rasa/duckling) running. 
Duckling is used to parse things like emails, dates, temporal intervals and more.

**Deploying C-4PM on a server**

## Sample questions

| Task                            | Question                                                                                                 | Answer |
|---------------------------------|----------------------------------------------------------------------------------------------------------|--------|
| Specification description in NL |                                                                                                          |        |
| Consistency checking            |                                                                                                          |        |
| Conformance checking            |                                                                                                          |        |   
| Model checking                  |                                                                                                          |        |   
| Restricted conformance checking | Find traces in which IV Antibiotics are given to the patient right after a lactic acid test is performed |        |   
| Restricted conformance checking | Find traces in which IV Antibiotics occurs right after LacticAcid is performed                           |        |   
| Restricted conformance checking | In which cases ER Triage occurs right after ER Registration?                                             |        |   

In which cases ER Triage occurs right after ER Registration?

Generalizacion capabilities: Direct "Find traces in which IV Antibiotics occurs right after LacticAcid is performed" and indirect "Find traces in which IV Antibiotics are given to the patient right after a lactic acid test is performed" queries return the same result. 


## Modifications to source libraries

### LTLf2DFA
- Adapted GPT prompt and RASA NLU training data to these proposal's objectives.
- Added support to the "absence" Declare template in the GPT `prompt`

### Declare4Py
- Added support to the `absence` and `existence two` templates in `LTLModel.py`so the templates can be used in different reasoning tasks.

## Limits on this Demo
- The parsing of natural language formulas to LTLf is limited to simple formulae. No conjunction or disjunction is yet 
supported by the translator. But both conjunction, disjunction, implication, etc. are well supported by the tools
used to perform the reasoning tasks.
- The consistency checking and model checking tasks are limited in terms of formula size. Too big formulae make the
satisfiability check too demanding and slow, which would make the use of the conversational interface unpleasant. 
Optimizing this is planned as future work so bigger models can be used.



