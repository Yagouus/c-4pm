import sys
import os
import pathlib

from src.Declare4Py.ProcessModels.DeclareModel import DeclareModel
from src.Declare4Py.ProcessMiningTasks.Discovery.DeclareMiner import DeclareMiner
from src.Declare4Py.D4PyEventLog import D4PyEventLog

# log_path = os.path.join("../../../", "tests", "test_logs", "Sepsis Cases.xes.gz")
event_log = D4PyEventLog(case_name="case:concept:name")
event_log.parse_xes_log('../declare4py_tests/tests/test_logs/Sepsis Cases.xes.gz')

discovery = DeclareMiner(log=event_log, consider_vacuity=False, min_support=1, itemsets_support=1,
                         max_declare_cardinality=2)
discovered_model: DeclareModel = discovery.run()

print(discovered_model.serialized_constraints)

test = """Existence2[Admission NC]
Chain Response[Admission NC, Release B]
Chain Response[Admission NC, Release A]
Chain Precedence[IV Liquid, Admission NC]
Chain Response[ER Registration, ER Triage]
Chain Precedence[Release A, Return ER]
Chain Precedence[ER Sepsis Triage, IV Antibiotics]
Chain Response[ER Sepsis Triage, IV Antibiotics]
Chain Precedence[Admission IC, Admission NC]
Chain Precedence[IV Antibiotics, Admission NC]
Chain Precedence[Admission NC, Release B]
Chain Response[Admission IC, Admission NC]
Chain Response[LacticAcid, Leucocytes]
Chain Precedence[ER Registration, ER Triage]"""

def dec_to_basic_nl(specification=""):
    nl_specification = ""

    # Iterate through the specification's constraints

    nl_specification += "\n"
    for line in test.splitlines():

        # Detect the type of template
        template = line.split(sep='[')[0]

        # Detect activities
        target = line.split(sep='[')[1]

        if len(target.split(sep=',')) > 1:
            target_0 = target.split(sep=',')[0]
            target_1 = target.split(sep=',')[1].split(sep=']')[0]
            # print(template, target_0, target_1)
        else:
            target_0 = target.split(sep=']')[0]
            # print(template, target_0)

        # Classify template
        match template:
            case 'Existence1 ':
                nl_specification += f"Eventually, {target_0} will happen."
            case 'Existence2':
                nl_specification += f"{target_0} will happen at least twice."

    return nl_specification


print(dec_to_basic_nl(test))


