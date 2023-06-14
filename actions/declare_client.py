import textwrap


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

def conformance_check(model, log):
    pass