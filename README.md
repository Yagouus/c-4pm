# 🤖 C-4PM: A Conversational agent for declarative Process Mining

![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![Repo Size](https://img.shields.io/github/repo-size/Sulstice/global-chem)
[![PyPI version](https://badge.fury.io/py/global-chem.svg)](https://badge.fury.io/py/global-chem)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

C-4PM is a conversational interface for Declarative Process Mining. 
It allows users to interact with a declarative process specification and its corresponding event log
to perform multiple reasoning tasks.

## 📖 Abstract

The effective presentation of process models to non-expert users in a way that allows them to understand
and query these models is a well-known research challenge. Conversational interfaces, with their low
expertise requirements, offer a potential solution. While procedural models like Petri nets are not ideal
for linguistic presentation, declarative models, specifically the Declare specification, provide a more
suitable option. This paper introduces C-4PM, the first conversational interface for declarative process
specifications. C-4PM facilitates tasks such as consistency, conformance, and model checking through a
conversation-driven modular pipeline. The feasibility of the tool was assessed through a preliminary
evaluation on a healthcare process.

## 💬 Usage

### Interactive and video demo
- An **interactive demo** of the tool can be tested [here](https://tec.citius.usc.es/c-4pm/) (if the demo seems not to be working, please [get in touch](mailto:yago.fontenla.seco@usc.es)).
- A **video demonstration** of the tool can be found in this [youtube link](https://youtu.be/A5gF3q1bQWQ).

### Supported tasks and sample questions

The following table presents the main task types supported by C-4PM with some exemplary queries for each of them taking as a base the [Sepsis event log](https://data.4tu.nl/articles/dataset/Sepsis_Cases_-_Event_Log/12707639).
The event log and Declare specification are understood as given, so no discovery is necessary.

<table>
    <tr>
        <td>Task</td>
        <td>Question</td>
        <td>Answer</td>
    </tr>
    <tr>
        <td rowspan=2>Specification description in NL</td>
        <td>Can you describe the process?</td>
        <td>Description of the process in NL</td>
    </tr>
    <tr>
        <td>Explain the process specification</td>
        <td>Description of the process in NL</td>
    </tr>
    <tr>
        <td rowspan=2>List activities</td>
        <td>List the activities in the process</td>
        <td>List of all possible activities</td>
    </tr>
    <tr>
        <td>What activities can be executed in the process?</td>
        <td>List of all possible activities</td>
    </tr>
    <tr>
        <td rowspan=2>Consistency checking</td>
        <td>Does the model accept any behavior?</td>
        <td>Consistency checking boolean</td>
    </tr>
    <tr>
        <td>Is there any possible trace that conforms to the model?</td>
        <td>Consistency checking boolean</td>
    </tr>
    <tr>
        <td rowspan=2>Conformance checking</td>
        <td>Can you give me some conformant traces?</td>
        <td>Examples of conformant traces</td>
    </tr>
    <tr>
        <td>What are the cases that conform to the model?</td>
        <td>Examples of conformant traces</td>
    </tr>
    <tr>
        <td rowspan=2>Non-conformance checking</td>
        <td>How many traces don&#39;t conform to the specification?</td>
        <td>Number and examples of non-conformant traces</td>
    </tr>
    <tr>
        <td>Are there any non conformant traces?</td>
        <td>Number and examples of non-conformant traces</td>
    </tr>
    <tr>
        <td rowspan=2>Model checking</td>
        <td>Is it possible that ER Triage occurs before IV Liquids?</td>
        <td>Boolean model checking and examples of that behavior in the log</td>
    </tr>
    <tr>
        <td>If Admission NC has not happened yet, can activity Release A happen?</td>
        <td>Boolean model checking and examples of that behavior in the log</td>
    </tr>
    <tr>
        <td rowspan=2>Restricted conformance checking</td>
        <td>Find traces in which IV Antibiotics occurs right after LacticAcid is performed</td>
        <td>Examples of traces in which that behavior happens</td>
    </tr>
    <tr>
        <td>In which cases ER Triage occurs right after ER Registration?</td>
        <td>Examples of traces in which that behavior happens</td>
    </tr>
</table>

## 🛠️ Installation

> **Warning**  
> Creating a virtual environment is highly recommended. For best compatibility this 
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

> **NOTE:**   NL2LTL can be used with a RASA engine or GPT. In this particular case, the GPT engine is used.
> However, if you want to use the RASA engine, for training a customized RASA language model with your own data, 
> you can do this by running the command 
> `rasa train --config data/config.yml --domain data/domain.yml --data data/nlu_training.yml` 
>in the directory `nl2ltl/engines/rasa`. More information can be found in the [NL2LTL repository](https://github.com/IBM/nl2ltl)

### Modifications to source libraries

**NL2LTL**
- Adapted GPT prompt and RASA NLU training data to fit this proposal's objectives.
- Added support to the `absence` and `precendence` templates in the GPT `prompt`

**Declare4Py**
- Added support to the `absence` and `existence two` templates in `LTLModel.py`so the templates can be used in different reasoning tasks.

## 🚀 Running C-4PM
The conversational agent can be run locally, or you may want to deploy it on an online server:

### Running C-4PM locally

To run C-4PM locally you need to:

1. Run Docker so Lydia will appropriately run in the background (each time Lydia is invoked it will create a new container, delete them when you finish
running C-4pm to save some space).
2. Activate your virtual environment. Place yourself on the C-4pm directory `cd /home/citius/c-4pm`
and launch the virtual environment `source ./venv/bin/activate`.
3. Train a Rasa NLU model if you've not done it before. This is done with the `rasa train` command. More info [here](#training-and-using-your-own-model).
4. Run the Rasa Actions server: Place yourself in the `actions` folder inside the project root folder with `cd actions` and run the command `rasa run actions`.
5. Run Rasa exposing the REST api: Go back go the main projects directory (`cd ..`) and run the command `rasa run --enable-api`
6. Run `python main.py` file.
7. Go into your browser to [`http://localhost:8080/`](http://localhost:8080/) and enjoy 🤓.

### Deploying C-4PM on a server

To deploy C-4PM on a server, the service configuration files are provided in the `service` folder. Specific code for making
the app work in a server is needed, so server-version files of the main file and dash callbacks are provided in the `server` folder.
Then, you need to:

- Copy the files in the `service` directory to their corresponding folders (given you are using Linux/Mac):
  - `cp service/c-4pm.service /etc/systemd/system/`
  - `cp service/c-4pm.script /usr/bin/`
- Give execution permit to both files: 
  - `chmod +x /usr/bin/c-4pm.script`
  - `chmod +x /etc/systemd/system/c-4pm.service` 
- Finally, run the service with `systemctl restart c-4pm.service` (if it is already running and you update the files this will restart it).

If you get any auth errors during the process, try using `sudo`.

> **Warning**  
> As no Rasa models are provided in the repo, you'll need to train a model when you try to deploy it on a server. 
> So remember to activate the virtual environment `source ./venv/bin/activate` and run `rasa train` once you pull this
> repository to your server.



## ⚠️ Limits on this Demo
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
- Even session storage is used, if multiple users use the chatbot at the same time, due to only one action server
running, some overlapping may occur. In case this happens, a simple refresh of the page will start a new conversation.

## ✍🏼 Citing C-4PM

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
  volume    = {3469},
  pages     = {112-116},
  url = {https://ceur-ws.org/Vol-3469/paper-20.pdf},
  publisher = {CEUR-WS.org},
  year      = {2023}
}
```

### Acknowledgement

This research was funded by the Spanish Ministry for Science, Innovation and Universities (grants TIN2017-84796-C2-1-R, PID2020-112623GB-I00, and PDC2021-121072-C21) and the Galician Ministry of Education, University and Professional Training (grants ED431C2018/29 and ED431G2019/04). All grants were co-funded by the European Regional Development Fund (ERDF/FEDER program).

