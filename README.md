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

## Usage

### Interactive and video demo
- An **interactive demo** of the tool can be tested [here](https://tec.citius.usc.es/c-4pm/) (if the demo seems not to be working, please [get in touch](mailto:yago.fontenla.seco@usc.es)).
- A **video demonstration** of the tool can be found in this [youtube link](https://youtu.be/A5gF3q1bQWQ).

### Supported tasks and sample questions

The following table presents the main task types supported by C-4PM with some exemplary queries for each of them taking as a base the [Sepsis event log](https://data.4tu.nl/articles/dataset/Sepsis_Cases_-_Event_Log/12707639).
The event log and Declare specification are understood as given, so no discovery is necessary.

| Task                            | Question                                                                       | Answer                                                          |
|---------------------------------|--------------------------------------------------------------------------------|-----------------------------------------------------------------|
| Specification description in NL | Can you describe the process?                                                  | Description of the process in NL                                |
|                                 | Explain the process specification                                              | Description of the process in NL                                |
| List activities                 | List the activities in the process                                             | List of all possible activities                                 |
|                                 | What activities can be executed in the process?                                | List of all possible activities                                 |
| Consistency checking            | Does the model accept any behavior?                                            | Consistency checking boolean                                    |
|                                 | Is there any possible trace that conforms to the model?                        | Consistency checking boolean                                    |
| Conformance checking            | Can you give me some conformant traces?                                        | Examples of conformant traces                                   |   
|                                 | What are the cases that conform to the model?                                  | Examples of conformant traces                                   |
| Non-conformance checking        | How many traces don't conform to the specification?                            | Number and examples of non-conformant traces                    |   
|                                 | Are there any non conformant traces?                                           | Number and examples of non-conformant traces                    |
| Model checking                  | Is it possible that ER Triage occurs before IV Liquids?                        | Boolean model checking and examples of that behavior in the log |
|                                 | If Admission NC has not happened yet, can activity Release A happen?           | Boolean model checking and examples of that behavior in the log |
| Restricted conformance checking | Find traces in which IV Antibiotics occurs right after LacticAcid is performed | Examples of traces in which that behavior happens               |   
|                                 | In which cases ER Triage occurs right after ER Registration?                   | Examples of traces in which that behavior happens               |   


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
`model_path = 'models/model-name.tar.gz'`.

**Customizing NL2LTL**

> **_NOTE:_**   NL2LTL can be used with a RASA engine or GPT. In this particular case, the GPT engine is used.
> However, if you want to use the RASA engine, for training a customized RASA language model with your own data, 
> you can do this by running the command 
> `rasa train --config data/config.yml --domain data/domain.yml --data data/nlu_training.yml` 
>in the directory `nl2ltl/engines/rasa`. More information can be found in the [NL2LTL repository](https://github.com/IBM/nl2ltl)

### Running C-4PM
The conversational agent can be run locally, or you may want to deploy it on an online server:

**Running C-4PM locally**

To run C-4PM locally you need to:

- Run Docker so Lydia will appropriately run in the background (each time Lydia is invoked it will create a new container, delete them when you finish
running C-4pm to save some space).
- Remember to activate your virtual environment.
- Run the Rasa actions server. This can be done with the command `rasa run actions` in the `actions` folder inside the project root folder `cd actions`.
- Go back to the main project's directory and run `main.py` file.
- Go into your browser to `http://localhost:8080/` and enjoy :).

**Deploying C-4PM on a server**

To deploy C-4PM as a service, the service configuration files are provided in the `service` folder. Then, you need to:

- Copy the files in the `service` directory to their corresponding folders (given you are using Linux/Mac):
  - `cp service/c-4pm.service /etc/systemd/system/`
  - `cp service/c-4pm.script /usr/bin/`
- Give execution permit to both files: 
  - `chmod +x /usr/bin/c-4pm.script`
  - `chmod +x /etc/systemd/system/c-4pm.service` 
- Finally, run the service with `systemctl restart c-4pm.service` (if it is already running and you update the files this will restart it).

If you get any auth errors during the process, try using `sudo`.


## Modifications to source libraries

### LTLf2DFA
- Adapted GPT prompt and RASA NLU training data to these proposal's objectives.
- Added support to the `absence` and `precendence` templates in the GPT `prompt`

### Declare4Py
- Added support to the `absence` and `existence two` templates in `LTLModel.py`so the templates can be used in different reasoning tasks.

## Limits on this Demo
- As C-4PM is still in active development, for offering a stable experience during this preliminary testing stages, 
the use of the tool is limited to the Sepsis use-case described in the paper. 
Both event log and process specification are given to the system by default, 
so the user can test the proposed reasoning tasks in a controlled environment.
- The parsing of natural language formulas to LTLf is limited to simple formulae. No conjunction or disjunction is yet 
supported by the translator. But both conjunction, disjunction, implication, etc. are well supported by the tools
used to perform the reasoning tasks.
- The consistency checking and model checking tasks are limited in terms of formula size. Too big formulae make the
satisfiability check too demanding and slow, which would make the use of the conversational interface unpleasant. 
Optimizing this is planned as future work so bigger models can be used.
- No session storage is used, so, if multiple users use the chatbot at the same time, some overlapping may occur. This
is being currently fixed. In case this happens, a simple refresh of the page will start a new conversation.

## Citing C-4PM

> **_NOTE:_**  Incomplete, will be updated after the conference proceedings are published.

```
@inproceedings{Fontenla-Seco23,
  author    = {Yago Fontenla-Seco and
               Sarah Winkler and
               Alessandro Gianola and
               Marco Montali and
               Manuel Lama and
               Alberto Bugarín-Diz},
  title     = {The Droid You’re Looking For: C-4PM, a Conversational Agent for Declarative Process Mining},
  booktitle = {{BPM} (PhD/Demos)},
  series    = {{CEUR} Workshop Proceedings},
  volume    = {},
  pages     = {},
  publisher = {CEUR-WS.org},
  year      = {2023}
}
```


