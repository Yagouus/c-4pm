import random

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import warnings

warnings.filterwarnings("ignore")


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")

        return []


class ActionBehaviorCheck(Action):

    def name(self) -> Text:
        return "action_behavior_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Run NL2LTLf
        utterance = str(tracker.latest_message['text'])
        connectors = list(tracker.get_latest_entity_values("connector"))

        print(connectors)

        # Remove possible spaces in the connectors
        for connector in connectors:
            x = connector.replace(" ", "")
            utterance = utterance.replace(connector, x)

        # NL2LTL and get formula and confidence
        from nl2ltl_client import run
        formula, confidence = run(utterance)

        # Check confidence in result
        if confidence < 0.7:
            dispatcher.utter_message(
                text="I'm not sure about the behaviour you are asking, can you please reformulate your question?.")
            return []

        if formula is None:
            dispatcher.utter_message(text="There are no cases in which that happens.")
            return []

        print(formula)
        print(formula.to_english())

        # Do behavior check
        import declare_client
        fact = declare_client.behavior_check_ltl(formula=str(formula), connectors=connectors)

        # If the behavior is not admissible, return immediately
        if not fact:
            dispatcher.utter_message(
                text=f"The specification of the process does not allow for that behavior.".capitalize())
            return []

        # Conformance checking with ltl
        from declare_client import conformance_check_ltl
        traces = conformance_check_ltl(str(formula), connectors)

        if len(traces) > 0:
            result_text = f"The specification allows for that behavior. " \
                          f"Here are some cases in which, {formula.to_english()}"
        else:
            dispatcher.utter_message(text="The specification allows for that behavior. "
                                          "However, there are no cases in which that happens.")
            return []

        # Convert traces to text
        text = ""
        for idx, t in enumerate(traces):
            text += "" + str(t).replace("'", "").replace("[", "").replace("]", "") + "\n\n"
            if idx >= 5:
                break

        # Add spaces back to the string
        for connector in connectors:
            x = connector.replace(" ", "").lower()
            result_text = result_text.replace(x, connector)

        # Return the message
        dispatcher.utter_message(
            text=f'{result_text} \n\n {text}')

        return []


class ActionQueryCheck(Action):

    def name(self) -> Text:
        return "action_query_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ltl = next(tracker.get_latest_entity_values("ltl"), None)
        dispatcher.utter_message(text="Your formula is: " + str(ltl))

        return []


class ActionConveySpecification(Action):

    def name(self) -> Text:
        return "action_convey_specification"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
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

        # TODO: Read model from file -> Check how they do it in Declare4py

        from declare_client import dec_to_basic_nl
        text = dec_to_basic_nl(test)

        print(text)

        prompt = f"""
        Your task is to generate a short summary of a declarative process specification. 
        The input text consists in a series of short sentences that specify each of the restrictions of the model.
        Perform referring expression generation and combine the following sentences into a better written text, 
        don't use lists or enumerations, write a rich and clear text. 
        ```{text}```
        """

        from openai_client import get_completion
        response = get_completion(prompt)
        dispatcher.utter_message(text=response)

        return []


class ActionConformanceCheck(Action):
    """

    """

    def name(self) -> Text:
        return "action_conformance_check"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Performs conformance checking based on a declarative specification and an event log.
        :param dispatcher:
        :param tracker:
        :param domain:
        :return: Nothing
        """

        # Run the conformance checking method
        from declare_client import conformance_check
        traces = conformance_check()

        # Create and dispatch the message to the user
        variants = list({str(t) for t in traces})
        examples = "\n\n".join(t.translate(str.maketrans("", "", "[]'")) for t in random.sample(variants, k=4))
        message = f"In total, there are {len(traces)} conformant traces. Here are some examples: \n\n{examples}"
        dispatcher.utter_message(text=message)

        return []
    

#thesis project 
# This class defines a custom action to count the number of conformant traces in an event log.
# It uses the 'conformance_check' function from the 'declare_client' library to obtain the traces,
# counts the number of these traces, and then sends this count back to the user.
class ActionCountConformantTraces(Action):

    # Define the name of the custom action
    def name(self) -> Text:
        return "action_count_conformant_traces"
    # The main function that will be executed when this action is triggered
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         # Import the 'conformance_check' function from 'declare_client' to perform conformance checking and get traces
        from declare_client import conformance_check
        traces = conformance_check()

        # Count the number of conformant traces and prepare the message to be sent to the user
        num_conformant_traces = len(traces)
        message = f"The number of conformant traces is {num_conformant_traces}."

        # Dispatch the message to the user
        dispatcher.utter_message(text=message)

        return []
    
class ActionNonConformantCheck(Action):
    def name(self) -> Text:
        return "action_non_conformant_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Performs conformance checking based on a declarative specification and an event log.
        :param dispatcher:
        :param tracker:
        :param domain:
        :return: Nothing
        """

        # Run the conformance checking method
        from declare_client import conformance_check
        traces = conformance_check(opposite=True)

        # Create and dispatch the message to the user
        variants = list({str(t) for t in traces})
        examples = "\n\n".join(t.translate(str.maketrans("", "", "[]'")) for t in random.sample(variants, k=4))
        message = f"In total, there are {len(traces)} NON-conformant traces. Here are some examples: \n\n{examples}"
        dispatcher.utter_message(text=message)

        return []


class ActionBehaviorSearch(Action):
    def name(self) -> Text:
        return "action_behavior_search"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Parse input data: Remove possible spaces in the connectors
        utterance = str(tracker.latest_message['text'])
        connectors = list(tracker.get_latest_entity_values("connector"))

        if len(connectors) == 0:
            dispatcher.utter_message(text=f"Please check you have written the name of the activities correctly.")
            return []

        for connector in connectors:
            x = connector.replace(" ", "")
            utterance = utterance.replace(connector, x)

        # NL2LTL and get formula and confidence
        from nl2ltl_client import run
        res = run(utterance)
        if res:
            formula, confidence = res
        else:
            dispatcher.utter_message(text=(f"I'm not sure I understood the behavior you are looking for. "
                                           "Can you please reformulate your question?"))
            return []

            # Check confidence in result if Rasa and GPT do not agree or GPT could not parse a formula
        # Check that NL2ltl and rasa agree on number of activities detected
        activities = [a.replace(')', '') for a in str(formula).split()[1:]]

        print("Formula:", formula)
        print("Connectors:", connectors)
        print("Activities GPT:", activities)

        if len(connectors) != len(activities) or formula is None:
            dispatcher.utter_message(text=(f"Are you sure {str(activities).strip('[]')} occur/s in the process? "
                                           "Please check you have written the name of the activities correctly."))
            return []

        # Conformance checking with ltl
        # Notify the user if there ar no conformant traces
        from declare_client import conformance_check_ltl
        if traces := conformance_check_ltl(str(formula), connectors):
            message = (f"In total, there are {len(traces)} traces in which, {formula.to_english()}".capitalize() +
                       f"\n\nHere are some examples: \n\n")
        else:
            dispatcher.utter_message(text="There are no cases in which that happens.")
            return []

        # Add spaces back to the string
        for connector in connectors:
            x = connector.replace(" ", "").lower()
            message = message.replace(x, connector)

        # Convert traces to text
        variants = list({str(t) for t in traces})
        text = "\n\n".join(t.translate(str.maketrans("", "", "[]'")) for t in random.choices(variants, k=4))

        # Return the message
        dispatcher.utter_message(text=message + text)

        return []


class ActionActivities(Action):

    def name(self) -> Text:
        return "action_activities"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        import declare_client
        activities = declare_client.list_activities()

        examples = "\n\n".join(t.translate(str.maketrans("", "", "[]'")) for t in activities)
        message = f"In total, there are {len(activities)} possible activities. Here they are: \n\n{examples}"

        # Return the message
        dispatcher.utter_message(text=message)

        return []


class ActionConsistencyCheck(Action):
    def name(self) -> Text:
        return "action_consistency_check"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import declare_client

        if declare_client.consistency_check():
            dispatcher.utter_message(text="Yes, the specification is consistent and allows for behavior.")
        else:
            dispatcher.utter_message(text="The specification is inconsistent, please, review it.")

        return []

