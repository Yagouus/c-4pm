# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

import nest_asyncio

nest_asyncio.apply()

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


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
        ltl = next(tracker.get_latest_entity_values("ltl"), None)
        dispatcher.utter_message(text="Your formula is: " + str(ltl))

        return []


class ActionQueryCheck(Action):

    def name(self) -> Text:
        return "action_behavior_check"

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
    def name(self) -> Text:
        return "action_conformance_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        from declare_client import conformance_check
        traces = conformance_check()

        dispatcher.utter_message(text="Here you have some conformant traces: " + traces)

        return []


class ActionBehaviorSearch(Action):
    def name(self) -> Text:
        return "action_behavior_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        utterance = str(tracker.latest_message['text'])

        connectors = list(tracker.get_latest_entity_values("connector"))
        mod_connectors = []

        for connector in connectors:
            x = connector.replace(" ", "")
            utterance = utterance.replace(connector, x)

        from nl2ltl_client import run
        ltlf_formulas = run(utterance)
        print(ltlf_formulas)

        result_text = f"Here are all the cases in which, {ltlf_formulas.to_english()}".capitalize()

        for connector in connectors:
            x = connector.replace(" ", "").lower()
            result_text = result_text.replace(x, connector)

        dispatcher.utter_message(text=result_text)

        return []

