# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import random
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

import nest_asyncio

nest_asyncio.apply()

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

        # Remove possible spaces in the connectors
        for connector in connectors:
            x = connector.replace(" ", "")
            utterance = utterance.replace(connector, x)

        # Do behavior check

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

        # Conformance checking with ltl
        from declare_client import conformance_check_ltl
        traces = conformance_check_ltl(str(formula), connectors)

        if len(traces) > 0:
            result_text = f"Here are some cases in which, {formula.to_english()}".capitalize()
        else:
            dispatcher.utter_message(text="There are no cases in which that happens.")
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
        #for connector in connectors:
        #    x = connector.replace(" ", "")
        #    utterance = utterance.replace(connector, x)

        # NL2LTL and get formula and confidence
        from nl2ltl_client import run
        formula, confidence = run(utterance)

        # Check confidence in result if Rasa and GPT do not agree or GPT could not parse a formula
        # Check that NL2ltl and rasa agree on number of activities detected
        activities = [a.replace(')', '') for a in str(formula).split()[1:]]

        print("Formula:", formula)
        print("Connectors:", connectors)
        print("Activities GPT:", activities)

        if len(connectors) != len(activities) or formula is None:
            dispatcher.utter_message(text=(f"Are you sure {str(activities).strip('[]')} occur/s in the process? "
                                           "Please check you have written the name of the activities correctly?"))
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



