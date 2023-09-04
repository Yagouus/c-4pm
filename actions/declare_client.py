import textwrap

import numpy as np
import pm4py

from src.Declare4Py.ProcessModels.LTLModel import LTLTemplate, LTLModel


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


def conformance_check(threshold=0.8, opposite=False):
    from src.Declare4Py.D4PyEventLog import D4PyEventLog
    from src.Declare4Py.ProcessModels.DeclareModel import DeclareModel

    event_log = D4PyEventLog(case_name="case:concept:name")
    event_log.parse_xes_log('../assets/Sepsis Cases.xes.gz')

    declare_model = DeclareModel().parse_from_file('../assets/model.decl')

    from src.Declare4Py.ProcessMiningTasks.ConformanceChecking.MPDeclareAnalyzer import MPDeclareAnalyzer
    from src.Declare4Py.ProcessMiningTasks.ConformanceChecking.MPDeclareResultsBrowser import MPDeclareResultsBrowser

    basic_checker = MPDeclareAnalyzer(log=event_log, declare_model=declare_model, consider_vacuity=True)
    conf_check_res: MPDeclareResultsBrowser = basic_checker.run()

    traces = []

    # Truth values for the second trace
    for idx in range(event_log.get_length()):
        conf = conf_check_res.get_metric(trace_id=idx, metric="state")
        perc = np.sum(conf) / len(conf)
        if not opposite:
            if perc > threshold:
                traces.append(event_log.attribute_log_projection(event_log.get_concept_name())[idx])
        else:
            if perc < threshold:
                traces.append(event_log.attribute_log_projection(event_log.get_concept_name())[idx])

    return traces


def conformance_check_ltl(formula, connectors):
    from src.Declare4Py.D4PyEventLog import D4PyEventLog
    from src.Declare4Py.ProcessMiningTasks.ConformanceChecking.LTLAnalyzer import LTLAnalyzer

    # Load event log
    event_log = D4PyEventLog()
    event_log.parse_xes_log('../assets/Sepsis Cases.xes.gz')

    # Detect and translate the type of template
    template, *activities = formula.strip('()').split()

    # If no activity has been properly detected by rasa, return empty list of traces
    cs = [c.replace(' ', '') for c in connectors]
    if not connectors or sorted(cs) != sorted(activities):
        return []

    # Convert NL2LTL syntax to Declare4Py syntax
    template_mapping = {
        'Existence': 'eventually_activity_a',
        'ExistenceTwo': 'existence_two_activity_a',
        'Absence': 'not_eventually_activity_a',
        'RespondedExistence': 'responded_existence',
        'Response': 'response',
        'Precedence': 'eventually_a_then_b',
        'ChainResponse': 'chain_response',
        'NotCoExistence': 'chain_response'
    }

    # Translate NL2LTL to Declare4Py syntax
    if template := template_mapping.get(template):
        dec_template = LTLTemplate(template)
        if template in ['eventually_activity_a', 'existence_two_activity_a', 'not_eventually_activity_a']:
            model = dec_template.fill_template([activities[0]])
        elif template in ['eventually_a_then_b']:
            model = dec_template.fill_template([activities[0], activities[1]])
        else:
            model = dec_template.fill_template([activities[0]], [activities[1]])
    else:
        return None

    # Perform conformance checking
    analyzer = LTLAnalyzer(event_log, model)
    df = analyzer.run()

    # Recover accepted cases from the log and filter those containing all activities in the constraint
    if accepted_cases := df.loc[df['accepted'], 'case:concept:name'].tolist():
        traces = pm4py.filter_trace_attribute_values(event_log.get_log(), 'concept:name', accepted_cases,
                                                     case_id_key='concept:name')
        for a in connectors:
            traces = pm4py.filter_event_attribute_values(traces, 'concept:name', {a}, case_id_key='concept:name')
        return pm4py.project_on_event_attribute(traces, 'concept:name')
    else:
        return []


def behavior_check_ltl(specification=None, formula=None, connectors=[]):
    from src.Declare4Py.D4PyEventLog import D4PyEventLog

    # Load event log
    event_log = D4PyEventLog()
    event_log.parse_xes_log('../assets/Sepsis Cases.xes.gz')

    # Detect and translate the type of template
    template, *activities = formula.strip('()').split()

    print(template)
    print(connectors)
    print(activities)

    # If no activity has been properly detected by rasa, return empty list of traces
    cs = [c.replace(' ', '') for c in connectors]
    if not connectors or sorted(cs) != sorted(activities):
        return []

    # Convert NL2LTL syntax to Declare4Py syntax
    template_mapping = {
        'Existence': 'eventually_activity_a',
        'ExistenceTwo': 'existence_two_activity_a',
        'Absence': 'not_eventually_activity_a',
        'RespondedExistence': 'responded_existence',
        'Response': 'response',
        'Precedence': 'eventually_a_then_b',
        'ChainResponse': 'chain_response',
        'NotCoExistence': 'chain_response'
    }

    # Translate NL2LTL to Declare4Py syntax
    if template := template_mapping.get(template):
        dec_template = LTLTemplate(template)
        if template in ['eventually_activity_a', 'existence_two_activity_a', 'not_eventually_activity_a']:
            model = dec_template.fill_template([activities[0]])
        elif template in ['eventually_a_then_b']:
            model = dec_template.fill_template([activities[0], activities[1]])
        else:
            model = dec_template.fill_template([activities[0]], [activities[1]])
    else:
        return None

    nl_specification = dec2ltl(specification)
    nl_specification.add_disjunction(model.formula)
    sat = nl_specification.check_satisfiability()
    print(nl_specification.formula)
    print(sat)
    return sat


def consistency_check(specification=None):
    nl_specification = dec2ltl(specification)
    sat = nl_specification.check_satisfiability()
    print(nl_specification.formula)
    print(sat)
    return sat


def list_activities():
    from src.Declare4Py.D4PyEventLog import D4PyEventLog
    from src.Declare4Py.ProcessModels.DeclareModel import DeclareModel

    event_log = D4PyEventLog(case_name="case:concept:name")
    event_log.parse_xes_log('../assets/Sepsis Cases.xes.gz')

    declare_model = DeclareModel().parse_from_file('../assets/model.decl')

    return declare_model.get_model_activities()


# UTILS

def dec2ltl(specification=None):
    test = ("""
                    Existence2[Admission NC]
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
                    Chain Precedence[ER Registration, ER Triage]
                """)

    if not specification:
        specification = test

    template_mapping = {
        'Existence': 'eventually_activity_a',
        'Existence2': 'existence_two_activity_a',
        'Absence': 'not_eventually_activity_a',
        'RespondedExistence': 'responded_existence',
        'Response': 'response',
        'Precedence': 'eventually_a_then_b',
        'Chain Precedence': 'chain_precedence',
        'Chain Response': 'chain_response',
        'NotCoExistence': 'chain_response'
    }

    nl_specification = None
    fixed_specification = textwrap.dedent(specification)

    lines = fixed_specification.splitlines()

    # Iterate through the specification's constraints
    for idx, line in enumerate(lines):

        if idx > 4:
            break

        if line:

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

            # Translate NL2LTL to Declare4Py syntax
            if template := template_mapping.get(template):
                dec_template = LTLTemplate(template)
                if template in ['eventually_activity_a', 'existence_two_activity_a', 'not_eventually_activity_a']:
                    t = dec_template.fill_template([target_0]).formula
                elif template in ['eventually_a_then_b']:
                    t = dec_template.fill_template([target_0, target_1]).formula
                else:
                    t = dec_template.fill_template([target_0], [target_1]).formula

            if nl_specification:
                nl_specification.add_disjunction(t)
            else:
                nl_specification = LTLModel()
                nl_specification.parse_from_string(t)
        else:
            nl_specification = nl_specification

    return nl_specification

# consistency_check()
# behavior_check_ltl(formula="RespondedExistence AdmissionNC ERTriage", connectors=["Admission NC", "ER Triage"])
