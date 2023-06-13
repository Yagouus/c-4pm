# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.openai_client import get_completion


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


class ActionTypeII(Action):

    def name(self) -> Text:
        return "action_type_ii"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        qualifier = next(tracker.get_latest_entity_values(entity_type="attribute", entity_role="qualifier"), None)
        summarizer = next(tracker.get_latest_entity_values(entity_type="attribute", entity_role="summarizer"), None)
        dispatcher.utter_message(
            text="Recognized qualifier: " + str(qualifier) + " - Recognized summarizer: " + str(summarizer))

        return []


class ConveySpecification(Action):

    def name(self) -> Text:
        return "action_convey_specification"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = f"""
        ER triage occurs at least once
        ER registration occurs at least once
        ER registration occurs at most once
        ER registration occurs exactly once
        ER sepsis triage occurs at most once
        ER registration or ER triage occur
        If ER registration occurs, then ER triage occurs as well
        If ER triage occurs, then ER registration occurs as well
        ER registration or ER Sepsis Triage occur
        ER Sepsis triage or ER registration occur
        Leucocytes or ER registration occur
        Leucocytes or ER Triage occur
        Leucocytes or ER sepsis triage occur
        ER registration or CRP occur
        CRP or ER triage occur
        ER sepsis triage or CRP occur
        CRP or ER sepsis triage occur
        Admission NC occurs two times
        Each time Admission NC occurs, Release B occurs immediately afterwards
        Each time Admission NC occurs, Release A occurs immediately afterwards
        Each time Admission NC occurs, then IV Liquid occurs immediately beforehand
        """

        prompt = f"""
        Your task is to generate a short summary of a declarative process specification. 
        The input text consists in a series of short sentences that specify each of the restrictions of the model.
        Perform referring expression generation and combine the following sentences into a better written text, 
        don't use lists or enumerations, write a rich and clear text. 
        ```{text}```
        """

        response = get_completion(prompt)
        dispatcher.utter_message(text=response)

        return []
