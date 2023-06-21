import textwrap

import numpy as np

from src.Declare4Py.ProcessModels.LTLModel import LTLTemplate


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


def conformance_check_ltl(ltlf, connectors):
    from src.Declare4Py.D4PyEventLog import D4PyEventLog
    from src.Declare4Py.ProcessModels.LTLModel import LTLModel
    from src.Declare4Py.ProcessMiningTasks.ConformanceChecking.LTLAnalyzer import LTLAnalyzer

    # Load event log
    event_log = D4PyEventLog()
    event_log.parse_xes_log('../assets/Sepsis Cases.xes.gz')

    activities = []

    # Detect and translate the type of template
    template = ltlf.split(sep=' ')[0].replace('(', '')
    activities.append(ltlf.split(sep=' ')[1].replace(')', ''))
    if len(ltlf.split(sep=' ')) > 2:
        activities.append(ltlf.split(sep=' ')[2].replace(')', ''))

    print(template)
    print(connectors)



    # If no activity has been properly detected by rasa, return empty list of traces
    if len(connectors) < 1:
        return []

    model = LTLModel()

    # Convert NL2LTL syntax to Declare4Py syntax
    match template:
        case 'Existence':
            model.parse_from_string(f'F({activities[0]})')

        case 'ExistenceTwo':
            dec_template = LTLTemplate('existence_two_activity_a')
            model = dec_template.fill_template([activities[0]])

        case 'Absence':
            dec_template = LTLTemplate('not_eventually_activity_a')
            model = dec_template.fill_template([activities[0]])

        case 'RespondedExistence':
            dec_template = LTLTemplate('responded_existence')
            model = dec_template.fill_template([activities[0]], [activities[1]])

        case 'Response':
            dec_template = LTLTemplate('response')
            model = dec_template.fill_template([activities[0]], [activities[1]])

        case 'Precedence':
            dec_template = LTLTemplate('precedence')
            model = dec_template.fill_template([activities[0]], [activities[1]])

        case 'ChainResponse':
            dec_template = LTLTemplate('chain_response')
            model = dec_template.fill_template([activities[0]], [activities[1]])

        case 'NotCoExistence':
            dec_template = LTLTemplate('chain_response')
            model = dec_template.fill_template([activities[0]], [activities[1]])

    analyzer = LTLAnalyzer(event_log, model)
    df = analyzer.run()

    # Recover cases from the log and project the trace
    import pm4py
    case_ids = list(df.query('accepted == True')['case:concept:name'])
    traces = pm4py.filter_trace_attribute_values(event_log.get_log(),
                                                 'concept:name',
                                                 case_ids,
                                                 case_id_key=' concept:name')

    print('Vacuosly accepted traces', len(traces))

    # Filter traces that vacuosely satisfy the constraints
    # A trace needs to contain both activities that make the constraint

    for connector in connectors:
        x = connector.replace(" ", "")
        print("X", x, "Connector", connector)
        for idx, a in enumerate(activities):
            print("A", a)
            activities[idx] = a.replace(x, connector)

    #print(activities)



    # TODO: Need to add spaces back to original name, or create a map
    for a in activities:
        traces = pm4py.filter_event_attribute_values(
            traces,
            'concept:name',
            {a},
            case_id_key='concept:name')

    tr_attr_values = pm4py.project_on_event_attribute(traces, 'concept:name')

    # print(df)
    # print(case_ids)
    # print('Total traces', len(df))
    # print('Accepted trace ids', len(case_ids))

    print('Accepted traces', len(traces))

    # text = "\n"
    # for idx, t in enumerate(tr_attr_values):
    #    text += "-" + str(t) + "\n\n"
    #    if idx >= 5:
    #        break
    # print(text)

    return tr_attr_values

# model_discovery()
# print(conformance_check())

# conformance_check_ltl("(ExistenceTwo ReleaseA)", ["ReleaseA"])
