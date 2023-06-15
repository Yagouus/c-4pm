import textwrap

import numpy as np


def dec_to_basic_nl(specification=""):
    nl_specification = ""
    fixed_specification = textwrap.dedent(specification)

    # Iterate through the specification's constraints
    for line in fixed_specification.splitlines():

        if line != "":

            # Remove leading whitespaces
            line = line.lstrip()

            # Detect the type of template
            template = line.split(sep='[')[0]

            # Detect activities
            target = line.split(sep='[')[1]

            if len(target.split(sep=',')) > 1:
                target_0 = target.split(sep=',')[0].strip()
                target_1 = target.split(sep=',')[1].split(sep=']')[0].strip()
                # print(template, target_0, target_1)
            else:
                target_0 = target.split(sep=']')[0].strip()
                # print(template, target_0)

            # Add line jump
            nl_specification += "\n"

            # Classify template
            match template:
                case 'Existence1':
                    nl_specification += f"Eventually, {target_0} will happen."
                case 'Existence2':
                    nl_specification += f"{target_0} will happen at least twice."
                case 'Absence':
                    nl_specification += f"{target_0} will never happen."
                case 'Absence2':
                    nl_specification += f"{target_0} will never happen twice."
                case 'Choice':
                    nl_specification += f"Activity {target_0} or activity {target_1} will eventually happen. "
                case 'Exclusive Choice':
                    nl_specification += (
                        f"Activity {target_0} or activity {target_1} will eventually happen, but not together. ")
                case 'Responded Existence':
                    nl_specification += (f"If {target_0} happens at least once then {target_1} has to happen or "
                                         f"happened before {target_0}.")
                case 'Response':
                    nl_specification += (
                        f"Whenever activity {target_0} happens, activity {target_1} has to happen "
                        f"eventually afterward.")
                case 'Chain Response':
                    nl_specification += (
                        f"Every time activity {target_0} happens, it must be directly followed by activity "
                        f"{target_1} (activity {target_1} can also follow other activities).")
                case 'Precedence':
                    nl_specification += (
                        f"Whenever activity {target_1} happens, activity {target_0} has to have happened "
                        f"before it.")
                case 'Chain Precedence':
                    nl_specification += (
                        f"Whenever activity {target_1} happens, it must be directly preceded by activity {target_0}.")
                case 'Not CoExistence':
                    nl_specification += f"Either activity {target_0} or {target_1} can happen, but not both."

    return nl_specification

def model_discovery():
    from src.Declare4Py.ProcessModels.DeclareModel import DeclareModel
    from src.Declare4Py.ProcessMiningTasks.Discovery.DeclareMiner import DeclareMiner
    from src.Declare4Py.D4PyEventLog import D4PyEventLog

    # log_path = os.path.join("../../../", "tests", "test_logs", "Sepsis Cases.xes.gz")
    event_log = D4PyEventLog(case_name="case:concept:name")
    event_log.parse_xes_log('../assets/Sepsis Cases.xes.gz')

    discovery = DeclareMiner(log=event_log, consider_vacuity=False, min_support=1, itemsets_support=1,
                             max_declare_cardinality=2)
    discovered_model: DeclareModel = discovery.run()

    print(discovered_model.serialized_constraints)

def conformance_check(threshold=0.8):

    from src.Declare4Py.D4PyEventLog import D4PyEventLog
    from src.Declare4Py.ProcessModels.DeclareModel import DeclareModel

    event_log = D4PyEventLog(case_name="case:concept:name")
    event_log.parse_xes_log('../assets/Sepsis Cases.xes.gz')

    declare_model = DeclareModel().parse_from_file('../assets/model.decl')

    model_constraints = declare_model.get_decl_model_constraints()

    print("Model constraints:")
    print("-----------------")
    for idx, constr in enumerate(model_constraints):
        print(idx, constr)

    from src.Declare4Py.ProcessMiningTasks.ConformanceChecking.MPDeclareAnalyzer import MPDeclareAnalyzer
    from src.Declare4Py.ProcessMiningTasks.ConformanceChecking.MPDeclareResultsBrowser import MPDeclareResultsBrowser

    basic_checker = MPDeclareAnalyzer(log=event_log, declare_model=declare_model, consider_vacuity=True)
    conf_check_res: MPDeclareResultsBrowser = basic_checker.run()

    traces = []

    # Truth values for the second trace
    for idx in range(event_log.get_length()):
        conf = conf_check_res.get_metric(trace_id=idx, metric="state")
        perc = np.sum(conf) / len(conf)
        if perc > threshold:
            traces.append(event_log.attribute_log_projection(event_log.get_concept_name())[idx])

    return traces

#model_discovery()
print(conformance_check())